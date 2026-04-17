from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from catalogue.models import Show, Location, Representation, Review
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
        location_id = request.POST.get('location')
        ticket_count = int(request.POST.get('ticket_count', 0))

        location = get_object_or_404(Location, id=location_id)

        # Validation : tickets <= location capacity
        if ticket_count > location.capacity:
            messages.error(request, f"Le nombre de tickets ({ticket_count}) ne peut pas dépasser la capacité de la salle ({location.capacity}).")
            locations = Location.objects.all()
            return render(request, 'prod/submit_show.html', {'locations': locations})

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
            bookable=False # Not bookable until admin adds prices and publishes
        )

        # Create first Representation (Pending approval too)
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
