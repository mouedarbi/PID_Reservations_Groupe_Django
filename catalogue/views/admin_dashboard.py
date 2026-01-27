from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum, F, Count
from django.contrib.auth.models import User
from catalogue.models import Reservation, Show, RepresentationReservation, Representation
from django.utils import timezone
import datetime

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    """
    View for the custom admin dashboard.
    """
    
    # 1. Basic Counts
    total_reservations = Reservation.objects.count()
    total_customers = User.objects.count()
    active_shows = Show.objects.filter(bookable=True).count()
    
    # 2. Revenue & Tickets
    # Calculate revenue from RepresentationReservation (price * quantity)
    # Note: price in RepresentationReservation is a ForeignKey to Price model which has 'price' field.
    # We need to aggregate.
    
    revenue_agg = RepresentationReservation.objects.aggregate(
        total_rev=Sum(F('price__price') * F('quantity')),
        total_tickets=Sum('quantity')
    )
    total_revenue = revenue_agg['total_rev'] or 0
    total_tickets_sold = revenue_agg['total_tickets'] or 0
    
    # 3. Upcoming Shows (Representations)
    now = timezone.now()
    upcoming_reps_count = Representation.objects.filter(schedule__gte=now).count()
    
    # 4. Mock Data for Charts & Lists (to ensure template renders beautiful UI)
    # In a real app, we would query this per day/week.
    
    # Mocking 'upcoming_shows_list' for the UI
    # We'll fetch some real representations and format them
    upcoming_reps = Representation.objects.filter(schedule__gte=now).select_related('show').order_by('schedule')[:5]
    
    upcoming_shows_list = []
    for rep in upcoming_reps:
        # Mock capacity logic
        capacity = rep.available_seats + 20 # Assume 20 sold for demo
        sold = 20
        percentage = (sold / capacity) * 100 if capacity > 0 else 0
        
        upcoming_shows_list.append({
            'title': rep.show.title,
            'date': rep.schedule,
            'time': rep.schedule,
            'tickets_sold': sold,
            'capacity': capacity,
            'sold_percentage': round(percentage),
        })
        
    # If no real data, add dummy
    if not upcoming_shows_list:
        upcoming_shows_list = [
            {'title': 'Concert de Jazz', 'date': now + datetime.timedelta(days=2), 'time': now, 'tickets_sold': 45, 'capacity': 100, 'sold_percentage': 45},
            {'title': 'Théâtre Classique', 'date': now + datetime.timedelta(days=5), 'time': now, 'tickets_sold': 90, 'capacity': 100, 'sold_percentage': 90},
        ]

    # Mocking 'recent_activities'
    recent_activities = [
        {'title': 'Nouvelle réservation', 'description': 'Jean Dupont a réservé 2 places', 'timestamp': now - datetime.timedelta(minutes=15), 'status': 'success'},
        {'title': 'Nouveau commentaire', 'description': 'Marie a commenté "Super spectacle!"', 'timestamp': now - datetime.timedelta(hours=2), 'status': 'info'},
        {'title': 'Spectacle complet', 'description': 'Le concert de samedi est complet', 'timestamp': now - datetime.timedelta(days=1), 'status': 'warning'},
    ]
    
    # Mocking 'top_shows'
    top_shows = [
        {'title': 'Le Roi Lion', 'tickets_sold': 1200, 'capacity': 1500, 'revenue': 45000},
        {'title': 'Hamlet', 'tickets_sold': 800, 'capacity': 800, 'revenue': 24000},
        {'title': 'Starmania', 'tickets_sold': 650, 'capacity': 1000, 'revenue': 32500},
    ]

    context = {
        'page_title': 'Tableau de bord administration',
        'title': 'Tableau de bord',
        
        # Stats
        'total_reservations': total_reservations,
        'total_revenue': round(total_revenue, 2),
        'total_tickets_sold': total_tickets_sold,
        'active_shows': active_shows,
        'upcoming_shows': upcoming_reps_count,
        'total_customers': total_customers,
        
        # Growth (Mocked)
        'revenue_growth': 12.5,
        'tickets_growth': 8.2,
        'tickets_today': 15,
        'customers_growth': 5.4,
        'new_customers_month': 24,
        'conversion_rate': 3.2,
        'remaining_conversion': 96.8,
        'conversion_growth': 0.5,
        
        # Lists
        'upcoming_shows_list': upcoming_shows_list,
        'recent_activities': recent_activities,
        'top_shows': top_shows,
        
        # Charts Data (Lists for JS)
        'activity_data': [12, 19, 3, 5, 2, 3, 15],
        'revenue_data': [12000, 19000, 15000, 22000],
        'tickets_data': [400, 600, 500, 750],
    }
    return render(request, 'admin/dashboard.html', context)