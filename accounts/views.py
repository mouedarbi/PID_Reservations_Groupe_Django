from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import UserSignUpForm, UserUpdateForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from catalogue.models import Affiliate, AffiliateTier

class UserUpdateView(UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy("accounts:user-profile")
    template_name = "user/update.html"

    def test_func(self):
        pkInURL = self.kwargs['pk']
        return self.request.user.is_authenticated and self.request.user.id==pkInURL or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, _("Vous n'avez pas l'autorisation d'accéder à cette page!"))
        return redirect('accounts:user-profile')

class UserSignUpView(UserPassesTestMixin, CreateView):
    form_class = UserSignUpForm
    success_url = reverse_lazy("accounts:login")
    template_name = "registration/signup.html"

    def test_func(self):
        return self.request.user.is_anonymous or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, _("Vous êtes déjà inscrit!"))
        return redirect('frontend:home')

@login_required
def profile(request):
    languages = {
        "fr": _("Français"),
        "en": _("English"),
        "nl": _("Nederlands"),
    }
    
    # Récupérer l'affiliation
    affiliate, created = Affiliate.objects.get_or_create(user=request.user)
    if not affiliate.tier:
        free_tier = AffiliateTier.objects.filter(name='Free').first()
        if free_tier:
            affiliate.tier = free_tier
            affiliate.save()

    # Secure against missing usermeta
    from catalogue.models import UserMeta
    user_meta, created_meta = UserMeta.objects.get_or_create(user=request.user, defaults={'langue': 'fr'})
    
    try:
        user_lang = user_meta.langue
        lang_display = languages.get(user_lang, _("Non définie"))
    except Exception:
        lang_display = _("Non définie")

    return render(request, 'user/profile.html', {
        "user_language" : lang_display,
        "affiliate": affiliate,
    })


@login_required
def delete(request, pk):
    if request.method == 'POST':
        method = request.POST.get('_method', '').upper()

        if method == 'DELETE':
            if request.user and request.user.id == pk:
                user = User.objects.get(id=request.user.id)
                user.delete()

                messages.success(request, _("Utilisateur supprimé avec succès."))
                logout(request)
            else:
                messages.error(request,
                               _("Suppression d'un autre compte interdite!"))

            return redirect('frontend:home')

    messages.error(request, _("Suppression interdite (méthode incorrecte)!"))

    return redirect('frontend:home')

from django.utils import timezone
from catalogue.models import Affiliate, AffiliateTier, ApiRequestLog

@login_required
def affiliate_dashboard(request):
    """
    Gère l'espace API / Affiliation de l'utilisateur.
    """
    # Récupérer ou créer le profil d'affilié
    affiliate, created = Affiliate.objects.get_or_create(user=request.user)
    
    # Génération de la clé API si demandée via POST
    if request.method == 'POST':
        if not affiliate.api_key:
            import uuid
            affiliate.api_key = str(uuid.uuid4()).replace('-', '')
            affiliate.save()
            messages.success(request, _("Votre clé API a été générée avec succès !"))
        return redirect('accounts:user-api')

    # Assigner le plan Free par défaut si aucun plan n'est défini
    if not affiliate.tier:
        free_tier = AffiliateTier.objects.filter(name='Free').first()
        if free_tier:
            affiliate.tier = free_tier
            affiliate.save()

    # Statistiques de consommation
    today = timezone.now().date()
    requests_today = ApiRequestLog.objects.filter(
        affiliate=affiliate, 
        created_at__date=today
    ).count()

    last_logs = ApiRequestLog.objects.filter(affiliate=affiliate)[:10]

    # Récupérer tous les plans pour l'affichage des offres
    all_tiers = AffiliateTier.objects.all().order_by('price')

    return render(request, 'user/api.html', {
        'affiliate': affiliate,
        'all_tiers': all_tiers,
    })

@login_required
def affiliate_usage(request):
    """
    Affiche uniquement les statistiques de consommation de l'API.
    """
    affiliate, _ = Affiliate.objects.get_or_create(user=request.user)
    
    today = timezone.now().date()
    requests_today = ApiRequestLog.objects.filter(
        affiliate=affiliate, 
        created_at__date=today
    ).count()

    last_logs = ApiRequestLog.objects.filter(affiliate=affiliate)[:20]

    return render(request, 'user/api_usage.html', {
        'affiliate': affiliate,
        'requests_today': requests_today,
        'last_logs': last_logs,
        'usage_percent': (requests_today / affiliate.tier.api_limit_daily) * 100 if affiliate.tier and affiliate.tier.api_limit_daily > 0 else 0
    })

@login_required
def become_producer(request):
    from catalogue.models import ProducerRequest
    from .forms.ProducerRequestForm import ProducerRequestForm

    # Check if user is already a producer
    if request.user.groups.filter(name='PRODUCER').exists() or request.user.is_superuser:
        messages.info(request, _("Vous êtes déjà producteur."))
        return redirect('frontend:home')
        
    # Check if a pending request exists
    pending_request = ProducerRequest.objects.filter(user=request.user, status='pending').first()
    if pending_request:
        messages.info(request, _("Vous avez déjà soumis une demande pour devenir producteur. Elle est en cours d'examen."))
        return render(request, 'user/become_producer.html', {'pending': True})

    if request.method == 'POST':
        form = ProducerRequestForm(request.POST)
        if form.is_valid():
            producer_req = form.save(commit=False)
            producer_req.user = request.user
            producer_req.save()
            messages.success(request, _("Votre demande pour devenir producteur a été soumise avec succès. Elle est en attente d'approbation."))
            return redirect('accounts:user-profile')
    else:
        # Pre-fill form with user info
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = ProducerRequestForm(initial=initial_data)

    return render(request, 'user/become_producer.html', {'form': form, 'pending': False})

@login_required
def become_critic(request):
    from catalogue.models import CriticRequest
    from .forms.CriticRequestForm import CriticRequestForm

    # Check if user is already a critic
    if request.user.groups.filter(name='PRESS_CRITIC').exists() or request.user.is_superuser:
        messages.info(request, _("Vous êtes déjà critique de presse."))
        return redirect('frontend:home')
        
    # Check if a pending request exists
    pending_request = CriticRequest.objects.filter(user=request.user, status='pending').first()
    if pending_request:
        messages.info(request, _("Vous avez déjà soumis une demande pour devenir critique. Elle est en cours d'examen."))
        return render(request, 'user/become_critic.html', {'pending': True})

    if request.method == 'POST':
        form = CriticRequestForm(request.POST)
        if form.is_valid():
            critic_req = form.save(commit=False)
            critic_req.user = request.user
            critic_req.save()
            messages.success(request, _("Votre demande pour devenir critique a été soumise avec succès. Elle est en attente d'approbation."))
            return redirect('accounts:user-profile')
    else:
        # Pre-fill form with user info
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        form = CriticRequestForm(initial=initial_data)

    return render(request, 'user/become_critic.html', {'form': form, 'pending': False})
