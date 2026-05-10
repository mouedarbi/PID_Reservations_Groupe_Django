from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from catalogue.models import Show, Location, Representation, Review, PressArticle
from catalogue.forms.ShowForm import ShowForm
from catalogue.utils.stats import get_show_stats
from django.utils.text import slugify
from django.utils import timezone
import time

def is_producer(user):
    return user.groups.filter(name='PRODUCER').exists() or user.is_superuser

@login_required
@user_passes_test(is_producer)
def prod_dashboard(request):
    shows = Show.objects.filter(producer=request.user).order_by('-created_at')
    shows_with_stats = []
    for show in shows:
        stats = get_show_stats(show)
        shows_with_stats.append({
            'show': show,
            'stats': stats
        })
    
    return render(request, 'prod/prod_dashboard.html', {
        'shows_with_stats': shows_with_stats
    })

@login_required
@user_passes_test(is_producer)
def prod_submit_show(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        poster = request.FILES.get('poster')
        duration = request.POST.get('duration')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        
        # Location logic: Existing ID or new data
        location_id = request.POST.get('location_id') # From autocomplete hidden field
        loc_name = request.POST.get('loc_name') # From autocomplete input
        loc_address = request.POST.get('loc_address')
        loc_postal = request.POST.get('loc_postal')
        loc_city = request.POST.get('loc_city')
        loc_website = request.POST.get('loc_website')
        loc_phone = request.POST.get('loc_phone')
        loc_capacity = request.POST.get('loc_capacity', '0')
        
        ticket_count_str = request.POST.get('ticket_count', '0')

        try:
            ticket_count = int(ticket_count_str) if ticket_count_str else 0
            
            # 1. Resolve Location
            location = None
            if location_id:
                location = get_object_or_404(Location, id=location_id)
            elif loc_name:
                # Create a new Location (marked as pending or directly if trusted)
                # First, ensure Locality exists
                from catalogue.models import Locality
                locality, _ = Locality.objects.get_or_create(
                    postal_code=loc_postal,
                    defaults={'locality': loc_city, 'locality_fr': loc_city}
                )
                
                slug_loc = slugify(loc_name)[:50] + "-" + str(int(time.time()))
                location = Location.objects.create(
                    slug=slug_loc,
                    designation=loc_name,
                    address=loc_address,
                    locality=locality,
                    website=loc_website,
                    phone=loc_phone,
                    capacity=int(loc_capacity) if loc_capacity else 0,
                    is_active=False # Inactif jusqu'à validation admin
                )
            
            if not location:
                messages.error(request, "Veuillez sélectionner ou créer une salle.")
                return redirect('catalogue:prod_submit_show')

            # Validation : tickets <= location capacity
            if ticket_count > location.capacity and location.capacity > 0:
                messages.error(request, f"Le nombre de tickets ({ticket_count}) ne peut pas dépasser la capacité de la salle ({location.capacity}).")
                return render(request, 'prod/submit_show.html', {
                    'locations': Location.objects.all(),
                    'show': {'title': title, 'description': description, 'duration': duration, 'location_id': int(location_id)},
                    'representation': {'total_seats': ticket_count, 'schedule': f"{date_str}T{time_str}"}
                })

            # Create Show (Pending)
            slug = slugify(title)[:50] + "-" + str(int(time.time()))
            show = Show.objects.create(
                slug=slug,
                title=title,
                description=description,
                poster=poster,
                duration=duration,
                location=location,
                producer=request.user,
                status='pending',
                created_in=timezone.now().year,
                bookable=False
            )

            # Create first Representation
            schedule_str = f"{date_str} {time_str}"
            schedule = timezone.make_aware(timezone.datetime.strptime(schedule_str, "%Y-%m-%d %H:%M"))
            
            Representation.objects.create(
                show=show,
                schedule=schedule,
                location=location,
                available_seats=ticket_count,
                total_seats=ticket_count
            )

            messages.success(request, "Votre spectacle a été soumis avec succès et est en attente d'approbation par l'administrateur.")
            return redirect('catalogue:prod_dashboard')

        except Exception as e:
            messages.error(request, f"Une erreur est survenue lors de la soumission : {str(e)}")
            return render(request, 'prod/submit_show.html', {
                'locations': Location.objects.all(),
                'show': {'title': title, 'description': description, 'duration': duration, 'location_id': int(location_id) if location_id else None},
                'representation': {'total_seats': ticket_count_str, 'schedule': f"{date_str}T{time_str}" if date_str and time_str else None}
            })

    locations = Location.objects.all()
    return render(request, 'prod/submit_show.html', {'locations': locations})

@login_required
@user_passes_test(is_producer)
def prod_edit_show(request, pk):
    show = get_object_or_404(Show, pk=pk, producer=request.user)
    
    if request.method == 'POST':
        show.title = request.POST.get('title')
        show.description = request.POST.get('description')
        if request.FILES.get('poster'):
            show.poster = request.FILES.get('poster')
        show.duration = request.POST.get('duration')
        
        # If pending, allow changing location and date too
        if show.status == 'pending':
            location_id = request.POST.get('location')
            show.location = get_object_or_404(Location, id=location_id)
            
            # Update representation
            rep = show.representations.first()
            if rep:
                date_str = request.POST.get('date')
                time_str = request.POST.get('time')
                ticket_count = int(request.POST.get('ticket_count', 0))
                
                if ticket_count <= show.location.capacity:
                    schedule_str = f"{date_str} {time_str}"
                    rep.schedule = timezone.make_aware(timezone.datetime.strptime(schedule_str, "%Y-%m-%d %H:%M"))
                    rep.location = show.location
                    rep.available_seats = ticket_count
                    rep.total_seats = ticket_count
                    rep.save()
        
        show.save()
        messages.success(request, "Spectacle mis à jour.")
        return redirect('catalogue:prod_dashboard')

    locations = Location.objects.all()
    # Get initial date/time from first representation
    rep = show.representations.first()
    context = {
        'show': show,
        'locations': locations,
        'representation': rep,
        'is_edit': True
    }
    return render(request, 'prod/submit_show.html', context)

@login_required
@user_passes_test(is_producer)
def prod_moderate_reviews(request):
    # Only reviews for shows belonging to this producer
    reviews = Review.objects.filter(show__producer=request.user).order_by('-created_at')
    
    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        action = request.POST.get('action')
        review = get_object_or_404(Review, id=review_id, show__producer=request.user)
        
        if action == 'approve':
            review.validated = True
            review.save()
            messages.success(request, "Avis approuvé.")
        elif action == 'reject':
            review.validated = False
            review.save()
            messages.success(request, "Avis rejeté.")
        
        return redirect('catalogue:prod_moderate_reviews')

    return render(request, 'prod/moderate_reviews.html', {'reviews': reviews})

@login_required
@user_passes_test(is_producer)
def prod_moderate_press_articles(request):
    """
    Vue permettant au producteur de modérer les articles de presse sur ses spectacles.
    """
    articles = PressArticle.objects.filter(show__producer=request.user).select_related('user', 'show').order_by('-created_at')
    
    context = {
        'page_title': 'Gérer les Articles de Presse',
        'articles': articles,
    }
    return render(request, 'prod/moderate_press_articles.html', context)

@login_required
@user_passes_test(is_producer)
def prod_validate_press_article(request, pk, action):
    """
    Vue pour approuver, refuser ou épingler un article de presse.
    """
    article = get_object_or_404(PressArticle, pk=pk, show__producer=request.user)
    
    if action == 'approve':
        article.validated = True
        messages.success(request, f"L'article '{article.title}' a été approuvé.")
    elif action == 'reject':
        article.validated = False
        messages.warning(request, f"L'article '{article.title}' a été mis en attente.")
    elif action == 'pin':
        article.is_pinned = not article.is_pinned
        status = "épinglé" if article.is_pinned else "désépinglé"
        messages.info(request, f"L'article a été {status}.")
    elif action == 'delete':
        article.delete()
        messages.error(request, "L'article a été supprimé.")
        return redirect('catalogue:prod_moderate_press_articles')
        
    article.save()
    return redirect('catalogue:prod_moderate_press_articles')

@login_required
@user_passes_test(is_producer)
def pin_review(request, review_id):
    """
    Vue pour épingler ou désépingler un avis.
    """
    # Sécurité : On s'assure que le producteur ne peut épingler que les avis de ses propres shows.
    review = get_object_or_404(Review, id=review_id, show__producer=request.user)
    
    # Inverse l'état d'épinglage
    review.is_pinned = not review.is_pinned
    review.save()
    
    if review.is_pinned:
        messages.success(request, "L'avis a été épinglé avec succès.")
    else:
        messages.info(request, "L'avis a été désépinglé.")
        
    return redirect('catalogue:prod_moderate_reviews')
