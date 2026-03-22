from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum, F, Count
from django.contrib.auth.models import User
from catalogue.models import Reservation, Show, RepresentationReservation, Representation, Artist, Type, Review, Location, Price
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

@user_passes_test(is_admin)
def admin_show_index(request):
    """
    View to list shows in the custom admin dashboard.
    """
    shows = Show.objects.all().select_related('location').order_by('-created_at')

    # Simple search
    search_query = request.GET.get('q')
    if search_query:
        shows = shows.filter(title__icontains=search_query)

    context = {
        'page_title': 'Gestion des Spectacles',
        'title': 'Spectacles',
        'shows': shows,
        'search_query': search_query,
    }
    return render(request, 'admin/show/index.html', context)

@user_passes_test(is_admin)
def admin_representation_index(request):
    """
    View to list representations in the custom admin dashboard.
    """
    representations = Representation.objects.all().select_related('show', 'location').order_by('-schedule')

    # Simple search by show title
    search_query = request.GET.get('q')
    if search_query:
        representations = representations.filter(show__title__icontains=search_query)

    context = {
        'page_title': 'Gestion des Représentations',
        'title': 'Représentations',
        'representations': representations,
        'search_query': search_query,
    }
    return render(request, 'admin/representation/index.html', context)

@user_passes_test(is_admin)
def admin_artist_index(request):
    """
    View to list artists in the custom admin dashboard.
    """
    artists = Artist.objects.all().order_by('lastname')

    # Search by firstname or lastname
    search_query = request.GET.get('q')
    if search_query:
        from django.db.models import Q
        artists = artists.filter(
            Q(firstname__icontains=search_query) | 
            Q(lastname__icontains=search_query)
        )

    context = {
        'page_title': 'Gestion des Artistes',
        'title': 'Artistes',
        'artists': artists,
        'search_query': search_query,
    }
    return render(request, 'admin/artist/index.html', context)

@user_passes_test(is_admin)
def admin_type_index(request):
    """
    View to list types in the custom admin dashboard.
    """
    types = Type.objects.all().order_by('type')

    # Search by type name
    search_query = request.GET.get('q')
    if search_query:
        types = types.filter(type__icontains=search_query)

    context = {
        'page_title': 'Gestion des Types',
        'title': 'Types',
        'types': types,
        'search_query': search_query,
    }
    return render(request, 'admin/type/index.html', context)

@user_passes_test(is_admin)
def admin_review_index(request):
    """
    View to list reviews in the custom admin dashboard.
    """
    reviews = Review.objects.all().select_related('user', 'show').order_by('-created_at')

    # Search by user or show title
    search_query = request.GET.get('q')
    if search_query:
        from django.db.models import Q
        reviews = reviews.filter(
            Q(user__username__icontains=search_query) | 
            Q(show__title__icontains=search_query)
        )

    context = {
        'page_title': 'Gestion des Avis',
        'title': 'Avis',
        'reviews': reviews,
        'search_query': search_query,
    }
    return render(request, 'admin/review/index.html', context)

@user_passes_test(is_admin)
def admin_location_index(request):
    """
    View to list locations in the custom admin dashboard.
    """
    locations = Location.objects.all().select_related('locality').order_by('designation')

    # Search by designation or slug
    search_query = request.GET.get('q')
    if search_query:
        from django.db.models import Q
        locations = locations.filter(
            Q(designation__icontains=search_query) | 
            Q(slug__icontains=search_query)
        )

    context = {
        'page_title': 'Gestion des Lieux',
        'title': 'Lieux',
        'locations': locations,
        'search_query': search_query,
    }
    return render(request, 'admin/location/index.html', context)

@user_passes_test(is_admin)
def admin_locality_index(request):
    """
    Vue pour lister les localités dans le dashboard admin personnalisé.
    """
    from catalogue.models.locality import Locality
    localities = Locality.objects.all().order_by('postal_code')

    # Recherche simple par code postal ou nom de localité
    search_query = request.GET.get('q')
    if search_query:
        from django.db.models import Q
        localities = localities.filter(
            Q(postal_code__icontains=search_query) | 
            Q(locality__icontains=search_query)
        )

    context = {
        'page_title': 'Gestion des Localités',
        'title': 'Localités',
        'localities': localities,
        'search_query': search_query,
    }
    return render(request, 'admin/locality/index.html', context)

@user_passes_test(is_admin)
def admin_reservation_index(request):
    """
    Vue pour lister les réservations dans le dashboard admin personnalisé.
    """
    from django.db.models import Sum, F
    reservations = Reservation.objects.all().select_related('user').annotate(
        total_amount=Sum(F('representation_reservations__price__price') * F('representation_reservations__quantity')),
        total_tickets=Sum('representation_reservations__quantity')
    ).order_by('-booking_date')

    # Recherche par nom d'utilisateur ou statut
    search_query = request.GET.get('q')
    if search_query:
        from django.db.models import Q
        reservations = reservations.filter(
            Q(user__username__icontains=search_query) | 
            Q(status__icontains=search_query)
        )

    context = {
        'page_title': 'Gestion des Réservations',
        'title': 'Réservations',
        'reservations': reservations,
        'search_query': search_query,
    }
    return render(request, 'admin/reservation/index.html', context)

@user_passes_test(is_admin)
def admin_reservation_detail(request, pk):
    """
    Vue pour afficher les détails d'une réservation.
    """
    from django.shortcuts import get_object_or_404
    from django.db.models import Sum, F
    reservation = get_object_or_404(
        Reservation.objects.select_related('user').annotate(
            total_amount=Sum(F('representation_reservations__price__price') * F('representation_reservations__quantity')),
            total_tickets=Sum('representation_reservations__quantity')
        ), 
        pk=pk
    )

    items = reservation.representation_reservations.all().select_related('representation__show', 'price')

    context = {
        'page_title': f'Détails Réservation #{reservation.id}',
        'title': f'Réservation #{reservation.id}',
        'reservation': reservation,
        'items': items,
    }
    return render(request, 'admin/reservation/detail.html', context)

@user_passes_test(is_admin)
def admin_user_index(request):
    """
    Vue pour lister les utilisateurs dans le dashboard admin personnalisé.
    """
    users = User.objects.all().order_by('-date_joined')

    # Recherche par nom d'utilisateur ou email
    search_query = request.GET.get('q')
    if search_query:
        from django.db.models import Q
        users = users.filter(
            Q(username__icontains=search_query) | 
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )

    context = {
        'page_title': 'Gestion des Utilisateurs',
        'title': 'Utilisateurs',
        'users': users,
        'search_query': search_query,
    }
    return render(request, 'admin/user/index.html', context)

@user_passes_test(is_admin)
def admin_group_index(request):
    """
    Vue pour lister les groupes dans le dashboard admin personnalisé.
    """
    from django.contrib.auth.models import Group
    groups = Group.objects.all().annotate(user_count=Count('user')).order_by('name')

    # Recherche par nom de groupe
    search_query = request.GET.get('q')
    if search_query:
        groups = groups.filter(name__icontains=search_query)

    context = {
        'page_title': 'Gestion des Groupes',
        'title': 'Groupes',
        'groups': groups,
        'search_query': search_query,
    }
    return render(request, 'admin/user/group_index.html', context)

@user_passes_test(is_admin)
def admin_price_index(request):
    """
    Vue pour lister les prix dans le dashboard admin personnalisé.
    """
    prices = Price.objects.all().order_by('type', 'price')

    # Recherche par type ou description
    search_query = request.GET.get('q')
    if search_query:
        from django.db.models import Q
        prices = prices.filter(
            Q(type__icontains=search_query) | 
            Q(description__icontains=search_query)
        )

    context = {
        'page_title': 'Gestion des Prix',
        'title': 'Prix',
        'prices': prices,
        'search_query': search_query,
    }
    return render(request, 'admin/price/index.html', context)

@user_passes_test(is_admin)
def admin_show_detail(request, pk):
    """
    Vue pour afficher les détails d'un spectacle et gérer ses prix.
    """
    from django.shortcuts import get_object_or_404, redirect
    from .models import ShowPrice
    
    show = get_object_or_404(Show.objects.select_related('location'), pk=pk)

    if request.method == 'POST':
        # Gérer l'ajout d'un prix
        price_id = request.POST.get('price_id')
        if price_id:
            price = get_object_or_404(Price, id=price_id)
            ShowPrice.objects.get_or_create(show=show, price=price)
        
        # Gérer la suppression d'un prix
        delete_price_id = request.POST.get('delete_price_id')
        if delete_price_id:
            show_price_to_delete = get_object_or_404(ShowPrice, pk=delete_price_id)
            if show_price_to_delete.show == show: # Sécurité
                show_price_to_delete.delete()

        return redirect('admin_show_detail', pk=show.id)

    # Récupérer les prix associés à ce spectacle via le modèle ShowPrice
    show_prices = show.showprice_set.select_related('price').all()
    
    # Récupérer tous les prix qui ne sont pas encore associés à ce spectacle
    existing_price_ids = [sp.price.id for sp in show_prices]
    available_prices = Price.objects.exclude(id__in=existing_price_ids)

    context = {
        'page_title': f'Détails : {show.title}',
        'title': show.title,
        'show': show,
        'show_prices': show_prices,
        'available_prices': available_prices,
    }
    return render(request, 'admin/show/detail.html', context)
