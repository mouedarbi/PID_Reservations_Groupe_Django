from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import gettext as _

from catalogue.models import Review, Reservation, RepresentationReservation, Show
from catalogue.forms.ReviewForm import ReviewForm

def index(request):
    reviews = Review.objects.all()
    title = _('Liste des critiques')
    return render(request, 'review/index.html', {'reviews': reviews, 'title': title})

def show(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        raise Http404(_('Critique inexistante'))
    
    title = _('Fiche d\'une critique')
    return render(request, 'review/show.html', {'review': review, 'title': title})

@login_required
@permission_required('catalogue.add_review', raise_exception=True)
def create(request):
    show_id = request.GET.get('show_id') or request.POST.get('show')
    show_obj = get_object_or_404(Show, id=show_id) if show_id else None
    
    initial_data = {}
    if show_id:
        initial_data['show'] = show_id

    # LOGIQUE MÉTIER DE RESTRICTION
    is_press = request.user.groups.filter(name='PRESS_CRITIC').exists()
    is_member = request.user.groups.filter(name='MEMBER').exists()
    
    if is_member and not is_press and not request.user.is_superuser:
        if not show_id:
            messages.error(request, _("Veuillez choisir un spectacle pour laisser un commentaire."))
            return redirect('frontend:show_list')
        
        has_reservation = RepresentationReservation.objects.filter(
            reservation__user=request.user,
            reservation__status__in=['Confirmed', 'Paid', 'Completed'],
            representation__show_id=show_id
        ).exists()
        
        if not has_reservation:
            messages.error(request, _("Vous ne pouvez commenter que les spectacles auxquels vous avez assisté."))
            return redirect('frontend:show_detail', pk=show_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.validated = False
            review.save()
            messages.success(request, _("Votre avis a été soumis avec succès et sera publié après validation."))
            return redirect('frontend:show_detail', pk=review.show.id)
        else:
            messages.error(request, _("Veuillez corriger les erreurs ci-dessous."))
    else:
        form = ReviewForm(initial=initial_data)

    return render(request, 'review/create.html', {'form': form, 'show': show_obj})

@login_required
@permission_required('catalogue.change_review', raise_exception=True)
def edit(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if not request.user == review.user:
        messages.error(request, _("Seul l'auteur peut modifier son message."))
        return redirect('frontend:show_detail', pk=review.show.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, _("Critique modifiée avec succès."))
            return redirect('frontend:show_detail', pk=review.show.id)
        else:
            messages.error(request, _("Veuillez corriger les erreurs ci-dessous."))
    else:
        form = ReviewForm(instance=review)

    return render(request, 'review/edit.html', {'form': form, 'review': review, 'show': review.show})

@login_required
@permission_required('catalogue.delete_review', raise_exception=True)
def delete(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    is_moderator = request.user.groups.filter(name__in=['PRODUCER', 'ADMINISTRATOR']).exists() or request.user.is_superuser
    
    if not (request.user == review.user or is_moderator):
        messages.error(request, _("Vous n'êtes pas autorisé à supprimer ce message."))
        return redirect('frontend:show_detail', pk=review.show.id)

    if request.method == 'POST':
        show_id = review.show.id
        review.delete()
        messages.success(request, _("Message supprimé avec succès."))
        return redirect('frontend:show_detail', pk=show_id)
    
    return render(request, 'review/delete_confirm.html', {'review': review})
