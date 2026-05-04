from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum, F, Count
from django.contrib.auth.models import User
from catalogue.models import Reservation, Show, RepresentationReservation, Representation, Artist, Type, Review, Location, Price, Locality, AppSetting, ArtistType, ShowPrice
from catalogue.utils.ticketmaster import run_ticketmaster_import, run_ticketmaster_import_gen
from django.http import StreamingHttpResponse
from payments.models import Payment
from catalogue.forms.ArtistForm import ArtistForm
from catalogue.forms.ShowForm import ShowForm
from catalogue.forms.LocationForm import LocationForm
from catalogue.forms.LocalityForm import LocalityForm
from catalogue.forms.PriceForm import PriceForm
from catalogue.forms.TypeForm import TypeForm
from catalogue.forms.ReviewForm import ReviewForm
from catalogue.forms.RepresentationForm import RepresentationForm
from catalogue.forms.ReservationForm import ReservationForm
from catalogue.forms.SettingForm import AppSettingForm
from catalogue.forms.ArtistTypeForm import ArtistTypeForm
from django.contrib.auth.models import Group
from accounts.forms.UserUpdateForm import UserUpdateForm
from accounts.forms.UserSignUpForm import UserSignUpForm
from accounts.forms.AdminUserUpdateForm import AdminUserUpdateForm
from accounts.forms.GroupForm import GroupForm
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
    pending_shows_count = Show.objects.filter(status='pending').count()
    
    # 2. Revenue & Tickets Sold
    # On calcule le revenu réel basé sur les paiements Stripe réussis
    total_revenue = Payment.objects.filter(status='succeeded').aggregate(total=Sum('amount'))['total'] or 0
    
    # Pour les tickets, on garde le calcul basé sur les réservations payées
    total_tickets_sold = RepresentationReservation.objects.filter(reservation__status='PAID').aggregate(total=Sum('quantity'))['total'] or 0
    
    # 3. Upcoming Shows (Representations)
    now = timezone.now()
    upcoming_reps_count = Representation.objects.filter(schedule__gte=now).count()
    
    # 4. Mock Data for Charts & Lists (to ensure template renders beautiful UI)
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

    # On récupère les 5 derniers paiements réels pour les activités
    recent_payments = Payment.objects.select_related('reservation__user').order_by('-created_at')[:5]
    
    recent_activities = []
    for payment in recent_payments:
        recent_activities.append({
            'title': 'Paiement Stripe',
            'description': f'{payment.reservation.user.username} a payé {payment.amount} {payment.currency}',
            'timestamp': payment.created_at,
            'status': 'success' if payment.status == 'succeeded' else 'warning'
        })
    
    # Si pas de paiements réels, on garde les mocks originaux
    if not recent_activities:
        recent_activities = [
            {'title': 'Nouvelle réservation', 'description': 'Jean Dupont a réservé 2 places', 'timestamp': now - datetime.timedelta(minutes=15), 'status': 'success'},
            {'title': 'Nouveau commentaire', 'description': 'Marie a commenté "Super spectacle!"', 'timestamp': now - datetime.timedelta(hours=2), 'status': 'info'},
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
        'pending_shows_count': pending_shows_count,
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
def admin_representation_detail(request, pk):
    """
    Vue pour afficher les détails d'une représentation (incluant les réservations).
    """
    representation = get_object_or_404(Representation.objects.select_related('show', 'location'), pk=pk)
    
    # Récupérer les réservations pour cette représentation spécifique
    reservations = RepresentationReservation.objects.filter(representation=representation).select_related('reservation__user', 'price')
    
    context = {
        'page_title': f'Détails Représentation : {representation.show.title}',
        'title': f'{representation.show.title} - {representation.schedule.strftime("%d/%m/%Y %H:%M")}',
        'representation': representation,
        'reservations': reservations,
    }
    return render(request, 'admin/representation/detail.html', context)

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
def admin_type_detail(request, pk):
    """
    View to display type details (artists having this type).
    """
    type_obj = get_object_or_404(Type, pk=pk)
    # Get artists having this type via ArtistType
    artists = Artist.objects.filter(a_artistTypes__type=type_obj).distinct()
    
    context = {
        'page_title': f'Détails Type : {type_obj.type}',
        'title': type_obj.type,
        'type': type_obj,
        'artists': artists,
    }
    return render(request, 'admin/type/detail.html', context)

@user_passes_test(is_admin)
def artist_type_list(request):
    """
    View to list artist-type mappings.
    """
    mappings = ArtistType.objects.all().select_related('artist', 'type').order_by('artist__lastname')
    context = {
        'page_title': 'Mappage Artiste-Type',
        'title': 'Associations Artistes & Types',
        'mappings': mappings,
    }
    return render(request, 'admin/artist_type/index.html', context)

@user_passes_test(is_admin)
def artist_type_create(request):
    """
    View to create a new artist-type mapping.
    """
    if request.method == 'POST':
        form = ArtistTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('artist_type_list')
    else:
        form = ArtistTypeForm()
    context = {
        'page_title': 'Ajouter un Mappage',
        'title': 'Nouvel Association Artiste-Type',
        'form': form,
    }
    return render(request, 'admin/artist_type/create.html', context)

@user_passes_test(is_admin)
def artist_type_edit(request, pk):
    """
    View to edit an existing artist-type mapping.
    """
    mapping = get_object_or_404(ArtistType, pk=pk)
    if request.method == 'POST':
        form = ArtistTypeForm(request.POST, instance=mapping)
        if form.is_valid():
            form.save()
            return redirect('artist_type_list')
    else:
        form = ArtistTypeForm(instance=mapping)
    context = {
        'page_title': 'Modifier Mappage',
        'title': 'Modifier Association Artiste-Type',
        'form': form,
        'mapping': mapping,
    }
    return render(request, 'admin/artist_type/edit.html', context)

@user_passes_test(is_admin)
def artist_type_delete(request, pk):
    """
    View to delete an artist-type mapping.
    """
    mapping = get_object_or_404(ArtistType, pk=pk)
    mapping.delete()
    return redirect('artist_type_list')

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
def admin_review_validate(request, pk):
    """
    Vue pour valider un avis.
    """
    review = get_object_or_404(Review, pk=pk)
    review.validated = True
    review.save()
    from django.contrib import messages
    messages.success(request, f"L'avis de {review.user.username} a été validé avec succès.")
    return redirect('admin_review_index')

@user_passes_test(is_admin)
def admin_review_reject(request, pk):
    """
    Vue pour rejeter un avis (le dévalider sans le supprimer).
    """
    review = get_object_or_404(Review, pk=pk)
    review.validated = False
    review.save()
    from django.contrib import messages
    messages.info(request, f"L'avis de {review.user.username} a été mis en attente.")
    return redirect('admin_review_index')

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
def admin_locality_detail(request, pk):
    """
    Vue pour afficher les détails d'une localité (incluant les lieux associés).
    """
    locality = get_object_or_404(Locality, pk=pk)
    locations = locality.locations.all()
    
    context = {
        'page_title': f'Détails Localité : {locality.locality}',
        'title': f'{locality.locality} ({locality.postal_code})',
        'locality': locality,
        'locations': locations,
    }
    return render(request, 'admin/locality/detail.html', context)

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
    
    # Récupérer le paiement associé si il existe
    payment = Payment.objects.filter(reservation=reservation).first()

    context = {
        'page_title': f'Détails Réservation #{reservation.id}',
        'title': f'Réservation #{reservation.id}',
        'reservation': reservation,
        'items': items,
        'payment': payment,
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
def admin_price_detail(request, pk):
    """
    Vue pour afficher les détails d'un prix (spectacles associés).
    """
    price = get_object_or_404(Price, pk=pk)
    # Get shows having this price via ShowPrice
    shows = Show.objects.filter(showprice__price=price).distinct()
    
    context = {
        'page_title': f'Détails Prix : {price.type}',
        'title': f'{price.type} ({price.price} €)',
        'price': price,
        'shows': shows,
    }
    return render(request, 'admin/price/detail.html', context)

@user_passes_test(is_admin)
def admin_show_detail(request, pk):
    """
    Vue pour afficher les détails d'un spectacle, gérer ses prix et ses représentations.
    """
    from django.shortcuts import get_object_or_404, redirect
    from catalogue.models import ShowPrice

    show = get_object_or_404(Show.objects.select_related('location'), pk=pk)

    # Récupérer les représentations existantes pour ce spectacle
    representations = show.representations.all().order_by('schedule')

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
        'representations': representations,
    }
    return render(request, 'admin/show/detail.html', context)
@user_passes_test(is_admin)
def admin_artist_detail(request, pk):
    """
    View to display artist details in the custom admin dashboard.
    """
    artist = get_object_or_404(Artist, pk=pk)
    
    # Récupérer les types associés à cet artiste via ArtistType
    artist_types = artist.a_artistTypes.all().select_related('type')
    
    context = {
        'page_title': f'Détails Artiste : {artist.firstname} {artist.lastname}',
        'title': f'{artist.firstname} {artist.lastname}',
        'artist': artist,
        'artist_types': artist_types,
    }
    return render(request, 'admin/artist/detail.html', context)

@user_passes_test(is_admin)
def admin_artist_create(request):
    """
    View to create a new artist in the custom admin dashboard.
    """
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_artist_index')
    else:
        form = ArtistForm()

    context = {
        'page_title': 'Ajouter un Artiste',
        'title': 'Ajouter un Artiste',
        'form': form,
    }
    return render(request, 'admin/artist/create.html', context)

@user_passes_test(is_admin)
def admin_artist_edit(request, pk):
    """
    View to edit an existing artist in the custom admin dashboard.
    """
    artist = get_object_or_404(Artist, pk=pk)
    
    if request.method == 'POST':
        form = ArtistForm(request.POST, instance=artist)
        if form.is_valid():
            form.save()
            return redirect('admin_artist_index')
    else:
        form = ArtistForm(instance=artist)

    context = {
        'page_title': f'Modifier Artiste : {artist.firstname} {artist.lastname}',
        'title': 'Modifier l\'Artiste',
        'artist': artist,
        'form': form,
    }
    return render(request, 'admin/artist/edit.html', context)

@user_passes_test(is_admin)
def admin_show_create(request):
    """
    View to create a new show in the custom admin dashboard.
    """
    if request.method == 'POST':
        form = ShowForm(request.POST, request.FILES)
        if form.is_valid():
            show = form.save(commit=False)
            show.status = 'published'
            show.save()
            form.save_m2m()
            return redirect('admin_show_index')
    else:
        form = ShowForm()

    context = {
        'page_title': 'Ajouter un Spectacle',
        'title': 'Ajouter un Spectacle',
        'form': form,
    }
    return render(request, 'admin/show/create.html', context)

@user_passes_test(is_admin)
def admin_show_edit(request, pk):
    """
    View to edit an existing show in the custom admin dashboard.
    """
    show = get_object_or_404(Show, pk=pk)
    
    if request.method == 'POST':
        form = ShowForm(request.POST, instance=show)
        if form.is_valid():
            form.save()
            return redirect('admin_show_index')
    else:
        form = ShowForm(instance=show)

    context = {
        'page_title': f'Modifier Spectacle : {show.title}',
        'title': 'Modifier le Spectacle',
        'show': show,
        'form': form,
    }
    return render(request, 'admin/show/edit.html', context)

# --- Locations CRUD ---

@user_passes_test(is_admin)
def admin_location_detail(request, pk):
    location = get_object_or_404(Location, pk=pk)
    context = {
        'page_title': f'Détails Lieu : {location.designation}',
        'title': location.designation,
        'location': location,
    }
    return render(request, 'admin/location/detail.html', context)

@user_passes_test(is_admin)
def admin_location_create(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_location_index')
    else:
        form = LocationForm()
    context = {
        'page_title': 'Ajouter un Lieu',
        'title': 'Ajouter un Lieu',
        'form': form,
    }
    return render(request, 'admin/location/create.html', context)

@user_passes_test(is_admin)
def admin_location_edit(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return redirect('admin_location_index')
    else:
        form = LocationForm(instance=location)
    context = {
        'page_title': f'Modifier Lieu : {location.designation}',
        'title': 'Modifier le Lieu',
        'location': location,
        'form': form,
    }
    return render(request, 'admin/location/edit.html', context)

# --- Localities CRUD ---

@user_passes_test(is_admin)
def admin_locality_create(request):
    if request.method == 'POST':
        form = LocalityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_locality_index')
    else:
        form = LocalityForm()
    context = {
        'page_title': 'Ajouter une Localité',
        'title': 'Ajouter une Localité',
        'form': form,
    }
    return render(request, 'admin/locality/create.html', context)

@user_passes_test(is_admin)
def admin_locality_edit(request, pk):
    locality = get_object_or_404(Locality, pk=pk)
    if request.method == 'POST':
        form = LocalityForm(request.POST, instance=locality)
        if form.is_valid():
            form.save()
            return redirect('admin_locality_index')
    else:
        form = LocalityForm(instance=locality)
    context = {
        'page_title': f'Modifier Localité : {locality.locality}',
        'title': 'Modifier la Localité',
        'locality': locality,
        'form': form,
    }
    return render(request, 'admin/locality/edit.html', context)

# --- Prices CRUD ---

@user_passes_test(is_admin)
def admin_price_create(request):
    if request.method == 'POST':
        form = PriceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_price_index')
    else:
        form = PriceForm()
    context = {
        'page_title': 'Ajouter un Prix',
        'title': 'Ajouter un Prix',
        'form': form,
    }
    return render(request, 'admin/price/create.html', context)

@user_passes_test(is_admin)
def admin_price_edit(request, pk):
    price = get_object_or_404(Price, pk=pk)
    if request.method == 'POST':
        form = PriceForm(request.POST, instance=price)
        if form.is_valid():
            form.save()
            return redirect('admin_price_index')
    else:
        form = PriceForm(instance=price)
    context = {
        'page_title': f'Modifier Prix : {price.type}',
        'title': 'Modifier le Prix',
        'price': price,
        'form': form,
    }
    return render(request, 'admin/price/edit.html', context)

# --- Types CRUD ---

@user_passes_test(is_admin)
def admin_type_create(request):
    if request.method == 'POST':
        form = TypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_type_index')
    else:
        form = TypeForm()
    context = {
        'page_title': 'Ajouter un Type',
        'title': 'Ajouter un Type',
        'form': form,
    }
    return render(request, 'admin/type/create.html', context)

@user_passes_test(is_admin)
def admin_type_edit(request, pk):
    type_obj = get_object_or_404(Type, pk=pk)
    if request.method == 'POST':
        form = TypeForm(request.POST, instance=type_obj)
        if form.is_valid():
            form.save()
            return redirect('admin_type_index')
    else:
        form = TypeForm(instance=type_obj)
    context = {
        'page_title': f'Modifier Type : {type_obj.type}',
        'title': 'Modifier le Type',
        'type': type_obj,
        'form': form,
    }
    return render(request, 'admin/type/edit.html', context)

# --- Reviews CRUD ---

@user_passes_test(is_admin)
def admin_review_edit(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('admin_review_index')
    else:
        form = ReviewForm(instance=review)
    context = {
        'page_title': f'Modifier Avis : {review.id}',
        'title': 'Modifier l\'Avis',
        'review': review,
        'form': form,
    }
    return render(request, 'admin/review/edit.html', context)

# --- Representations CRUD ---

@user_passes_test(is_admin)
def admin_representation_create(request):
    show_id = request.GET.get('show_id')
    show = None
    if show_id:
        show = get_object_or_404(Show, id=show_id)

    if request.method == 'POST':
        form = RepresentationForm(request.POST)
        if form.is_valid():
            representation = form.save()
            if show:
                return redirect('admin_show_detail', pk=show.id)
            return redirect('admin_representation_index')
    else:
        initial_data = {}
        if show:
            initial_data['show'] = show
            initial_data['location'] = show.location
        form = RepresentationForm(initial=initial_data)
        
    context = {
        'page_title': 'Ajouter une Représentation',
        'title': 'Ajouter une Représentation',
        'form': form,
        'show': show,
    }
    return render(request, 'admin/representation/create.html', context)

@user_passes_test(is_admin)
def admin_representation_edit(request, pk):
    representation = get_object_or_404(Representation, pk=pk)
    if request.method == 'POST':
        form = RepresentationForm(request.POST, instance=representation)
        if form.is_valid():
            form.save()
            return redirect('admin_representation_index')
    else:
        form = RepresentationForm(instance=representation)
    context = {
        'page_title': f'Modifier Représentation : {representation.id}',
        'title': 'Modifier la Représentation',
        'representation': representation,
        'form': form,
    }
    return render(request, 'admin/representation/edit.html', context)

# --- Reservations CRUD ---

@user_passes_test(is_admin)
def admin_reservation_edit(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('admin_reservation_index')
    else:
        form = ReservationForm(instance=reservation)
    context = {
        'page_title': f'Modifier Réservation : #{reservation.id}',
        'title': 'Modifier la Réservation',
        'reservation': reservation,
        'form': form,
    }
    return render(request, 'admin/reservation/edit.html', context)

# --- Users & Groups CRUD ---

@user_passes_test(is_admin)
def admin_user_create(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_user_index')
    else:
        form = UserSignUpForm()
    context = {
        'page_title': 'Ajouter un Utilisateur',
        'title': 'Ajouter un Utilisateur',
        'form': form,
    }
    return render(request, 'admin/user/create.html', context)

@user_passes_test(is_admin)
def admin_user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = AdminUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_user_index')
    else:
        form = AdminUserUpdateForm(instance=user)
    context = {
        'page_title': f'Modifier Utilisateur : {user.username}',
        'title': 'Modifier l\'Utilisateur',
        'user_obj': user,
        'form': form,
    }
    return render(request, 'admin/user/edit.html', context)

@user_passes_test(is_admin)
def admin_user_detail(request, pk):
    """
    Vue détaillée pour un utilisateur (réservations et avis).
    """
    user_obj = get_object_or_404(User, pk=pk)
    
    # Réservations de l'utilisateur
    reservations = Reservation.objects.filter(user=user_obj).annotate(
        total_amount=Sum(F('representation_reservations__price__price') * F('representation_reservations__quantity')),
        total_tickets=Sum('representation_reservations__quantity')
    ).order_by('-booking_date')
    
    # Avis de l'utilisateur
    reviews = Review.objects.filter(user=user_obj).select_related('show').order_by('-created_at')
    
    context = {
        'page_title': f'Détails Utilisateur : {user_obj.username}',
        'title': user_obj.username,
        'user_obj': user_obj,
        'reservations': reservations,
        'reviews': reviews,
    }
    return render(request, 'admin/user/detail.html', context)

@user_passes_test(is_admin)
def admin_group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_group_index')
    else:
        form = GroupForm()
    context = {
        'page_title': 'Ajouter un Groupe',
        'title': 'Ajouter un Groupe',
        'form': form,
    }
    return render(request, 'admin/user/group_create.html', context)

@user_passes_test(is_admin)
def admin_group_edit(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('admin_group_index')
    else:
        form = GroupForm(instance=group)
    context = {
        'page_title': f'Modifier Groupe : {group.name}',
        'title': 'Modifier le Groupe',
        'group': group,
        'form': form,
    }
    return render(request, 'admin/user/group_edit.html', context)

@user_passes_test(is_admin)
def admin_group_detail(request, pk):
    """
    Vue détaillée pour un groupe (liste des membres et permissions).
    """
    group = get_object_or_404(Group, pk=pk)
    users = group.user_set.all()
    permissions = group.permissions.all().select_related('content_type').order_by('content_type__app_label', 'codename')
    
    context = {
        'page_title': f'Détails Groupe : {group.name}',
        'title': group.name,
        'group': group,
        'users': users,
        'permissions': permissions,
    }
    return render(request, 'admin/user/group_detail.html', context)

# --- Soft Delete Placeholder ---

@user_passes_test(is_admin)
def admin_generic_delete(request, model_name, pk):
    """
    Placeholder for soft delete.
    In the future, this will set is_deleted=True instead of deleting.
    """
    model_map = {
        'artist': Artist,
        'show': Show,
        'representation': Representation,
        'location': Location,
        'locality': Locality,
        'price': Price,
        'type': Type,
        'review': Review,
        'reservation': Reservation,
        'user': User,
        'group': Group,
    }
    
    model = model_map.get(model_name)
    if not model:
        return redirect('admin_dashboard')
        
    obj = get_object_or_404(model, pk=pk)
    
    # Check if model has is_deleted field
    if hasattr(obj, 'is_deleted'):
        obj.is_deleted = True
        obj.save()
    else:
        # For now, if no is_deleted field, just delete (to be changed when Soft Delete is implemented)
        obj.delete()
        
    return redirect(f'admin_{model_name}_index')

@user_passes_test(is_admin)
def admin_settings(request):
    """
    Vue pour gérer les paramètres de l'application (API Keys, etc.).
    """
    # Nettoyage : Supprimer l'ancienne clé Google si elle existe
    AppSetting.objects.filter(key='GOOGLE_TRANSLATE_API_KEY').delete()

    # S'assurer que les clés de base existent pour LibreTranslate
    AppSetting.objects.get_or_create(
        key='LIBRETRANSLATE_API_URL',
        defaults={'value': 'http://localhost:5000', 'description': 'URL de l\'instance LibreTranslate (ex: http://localhost:5000)'}
    )
    AppSetting.objects.get_or_create(
        key='LIBRETRANSLATE_API_KEY',
        defaults={'value': '', 'description': 'Clé API LibreTranslate (laisser vide si auto-hébergé)'}
    )

    # Paramètres Stripe
    AppSetting.objects.get_or_create(
        key='STRIPE_PUBLISHABLE_KEY',
        defaults={'value': '', 'description': 'Clé publique Stripe (pk_...)'}
    )
    AppSetting.objects.get_or_create(
        key='STRIPE_SECRET_KEY',
        defaults={'value': '', 'description': 'Clé secrète Stripe (sk_...)'}
    )

    # Paramètres Ticketmaster
    AppSetting.objects.get_or_create(
        key='TICKETMASTER_API_KEY',
        defaults={'value': '', 'description': 'Clé API Ticketmaster (Discovery API v2)'}
    )
    
    settings = AppSetting.objects.all().order_by('key')
    setting_forms = []
    
    # On initialise un formulaire soumis (s'il existe) et les autres avec leurs valeurs de BDD
    for s in settings:
        if request.method == 'POST' and str(s.id) == request.POST.get('setting_id'):
            # Formulaire qui vient d'être soumis
            form = AppSettingForm(request.POST, instance=s)
            if form.is_valid():
                form.save()
                from django.contrib import messages
                messages.success(request, f"Le paramètre {s.key} a été mis à jour.")
                return redirect('admin_settings')
            else:
                from django.contrib import messages
                messages.error(request, f"Erreur de validation pour {s.key}.")
                setting_forms.append({'obj': s, 'form': form}) # On garde le form avec ses erreurs
        else:
            # Formulaires normaux
            setting_forms.append({'obj': s, 'form': AppSettingForm(instance=s)})

    context = {
        'page_title': 'Paramètres de l\'application',
        'title': 'Paramètres Système',
        'settings': settings,
        'setting_forms': setting_forms,
    }
    return render(request, 'admin/settings/index.html', context)

@user_passes_test(is_admin)
def admin_payment_index(request):
    """
    Vue pour lister les paiements Stripe dans le dashboard admin personnalisé.
    """
    payments = Payment.objects.all().select_related('reservation__user').order_by('-created_at')

    # Recherche par nom d'utilisateur ou ID de session
    search_query = request.GET.get('q')
    if search_query:
        from django.db.models import Q
        payments = payments.filter(
            Q(reservation__user__username__icontains=search_query) | 
            Q(stripe_session_id__icontains=search_query) |
            Q(stripe_payment_intent_id__icontains=search_query)
        )

    context = {
        'page_title': 'Gestion des Paiements Stripe',
        'title': 'Paiements',
        'payments': payments,
        'search_query': search_query,
    }
    return render(request, 'admin/payment/index.html', context)

@user_passes_test(is_admin)
def admin_ticketmaster_sync(request):
    """
    Vue pour déclencher la synchronisation avec Ticketmaster.
    """
    try:
        count_new, count_updated = run_ticketmaster_import()
        from django.contrib import messages
        messages.success(request, f"Synchronisation terminée ! {count_new} nouveaux spectacles importés, {count_updated} mis à jour.")
    except Exception as e:
        from django.contrib import messages
        messages.error(request, f"Erreur lors de la synchronisation : {str(e)}")
        
    return redirect('admin_show_index')

@user_passes_test(is_admin)
def admin_ticketmaster_sync_live(request):
    """
    Vue de streaming pour afficher les logs de synchronisation en temps réel.
    """
    def stream_logs():
        # On utilise le générateur créé dans ticketmaster.py
        for message in run_ticketmaster_import_gen():
            yield message
            
    return StreamingHttpResponse(stream_logs(), content_type='text/plain')

@user_passes_test(is_admin)
def admin_producer_requests(request):
    """
    Vue pour lister les demandes pour devenir producteur.
    """
    from catalogue.models import ProducerRequest
    pending_requests = ProducerRequest.objects.filter(status='pending').order_by('-created_at')
    
    context = {
        'page_title': 'Demandes Producteurs Juniors',
        'title': 'Producteurs Juniors',
        'pending_requests': pending_requests,
    }
    return render(request, 'admin/producer_request/pending.html', context)

@user_passes_test(is_admin)
def admin_producer_request_action(request, pk, action):
    """
    Vue pour approuver ou rejeter une demande de producteur.
    """
    from catalogue.models import ProducerRequest
    from django.contrib.auth.models import Group
    
    req = get_object_or_404(ProducerRequest, pk=pk)
    
    if action == 'approve':
        req.status = 'approved'
        req.save()
        # Add user to PRODUCER group
        producer_group, _ = Group.objects.get_or_create(name='PRODUCER')
        req.user.groups.add(producer_group)
        
        # Remove user from MEMBER group if they are in it
        member_group = Group.objects.filter(name='MEMBER').first()
        if member_group:
            req.user.groups.remove(member_group)
            
        from django.contrib import messages
        messages.success(request, f"La demande de {req.first_name} {req.last_name} a été acceptée. L'utilisateur est maintenant Producteur.")
    elif action == 'reject':
        req.status = 'rejected'
        req.save()
        from django.contrib import messages
        messages.success(request, f"La demande de {req.first_name} {req.last_name} a été refusée.")
        
    return redirect('admin_producer_requests')

@user_passes_test(is_admin)
def admin_pending_shows(request):
    """
    Vue pour lister les spectacles en attente de validation.
    """
    pending_shows = Show.objects.filter(status='pending').select_related('producer', 'location').order_by('-created_at')
    
    context = {
        'page_title': 'Spectacles en attente',
        'title': 'Modération des Spectacles',
        'pending_shows': pending_shows,
    }
    return render(request, 'admin/show/pending.html', context)

@user_passes_test(is_admin)
def admin_approve_show(request, pk):
    """
    Vue pour modifier, ajouter des prix et publier un spectacle soumis par un producteur.
    """
    show = get_object_or_404(Show, pk=pk)
    # On récupère la première représentation créée par le producteur (ou toutes)
    representations = show.representations.all()

    if request.method == 'POST':
        # 1. Mise à jour des infos de base (SEULEMENT si présentes dans le POST)
        # Cela évite d'écraser avec None quand on ajoute juste un prix via l'autre formulaire
        new_title = request.POST.get('title')
        new_duration = request.POST.get('duration')
        new_location_id = request.POST.get('location')

        if new_title:
            show.title = new_title
        if new_duration:
            show.duration = new_duration
        if new_location_id:
            show.location_id = new_location_id
        
        # 2. Tentative de Publication
        if 'publish' in request.POST:
            # Vérification de TOUS les champs requis
            rep = representations.first()
            date_val = request.POST.get('date')
            time_val = request.POST.get('time')
            
            if not all([show.title, show.duration, show.location_id, date_val, time_val]):
                from django.contrib import messages
                messages.error(request, "Impossible de publier : tous les champs (titre, durée, lieu, date, heure) doivent être remplis.")
            elif not show.prices.exists():
                from django.contrib import messages
                messages.error(request, "Impossible de publier : vous devez d'abord ajouter au moins un prix.")
            else:
                show.status = 'published'
                show.bookable = True
                show.save()
                from django.contrib import messages
                messages.success(request, f"Le spectacle '{show.title}' a été publié avec succès.")
                return redirect('admin_pending_shows')
        
        show.save()
        
        # 3. Mise à jour de la représentation
        # On n'effectue la mise à jour que si les champs sont présents dans le POST
        if representations.exists():
            rep = representations.first()
            date_str = request.POST.get('date')
            time_str = request.POST.get('time')
            ticket_count_str = request.POST.get('ticket_count')
            
            if date_str and time_str:
                try:
                    schedule_str = f"{date_str} {time_str}"
                    rep.schedule = timezone.make_aware(timezone.datetime.strptime(schedule_str, "%Y-%m-%d %H:%M"))
                    rep.location_id = show.location_id
                    
                    if ticket_count_str:
                        rep.total_seats = int(ticket_count_str)
                        rep.available_seats = int(ticket_count_str)
                    
                    rep.save()
                except ValueError as e:
                    from django.contrib import messages
                    messages.error(request, f"Format de date ou d'heure invalide : {e}")

        # 4. Ajout de prix (via ShowPrice)
        price_id = request.POST.get('price_id')
        if price_id:
            price = get_object_or_404(Price, id=price_id)
            from catalogue.models import ShowPrice
            ShowPrice.objects.get_or_create(show=show, price=price)

        return redirect('admin_approve_show', pk=show.id)

    locations = Location.objects.all()
    available_prices = Price.objects.all()
    show_prices = show.showprice_set.select_related('price').all()

    context = {
        'page_title': f'Approuver : {show.title}',
        'title': 'Validation de Spectacle',
        'show': show,
        'representations': representations,
        'locations': locations,
        'available_prices': available_prices,
        'show_prices': show_prices,
    }
    return render(request, 'admin/show/approve.html', context)


import csv
import io
from django.http import HttpResponse

@user_passes_test(is_admin)
def admin_export_shows_csv(request):
    """
    Exporte la liste des spectacles en format CSV.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="shows_export.csv"'
    
    # UTF-8 avec BOM pour Excel Windows
    response.write(u'\ufeff'.encode('utf8'))
    
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Slug', 'Titre', 'Description', 'Image URL', 'Lieu', 'Réservable', 'Statut'])
    
    for show in Show.objects.all():
        writer.writerow([
            show.id, 
            show.slug, 
            show.title, 
            show.description, 
            show.poster_url, 
            show.location.designation if show.location else '', 
            show.bookable, 
            show.status
        ])
    
    return response

@user_passes_test(is_admin)
def admin_import_shows_csv(request):
    """
    Importe des spectacles à partir d'un fichier CSV.
    """
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        # Vérification extension
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Le fichier doit être au format .csv")
            return redirect('admin_show_index')
            
        try:
            data_set = csv_file.read().decode('UTF-8-sig')
            io_string = io.StringIO(data_set)
            next(io_string) # Sauter l'en-tête
            
            count = 0
            for column in csv.reader(io_string, delimiter=';'):
                # Format attendu: Slug; Titre; Description; Image; Lieu_ID; Réservable(True/False); Statut
                # On utilise update_or_create basé sur le slug
                obj, created = Show.objects.update_or_create(
                    slug=column[1],
                    defaults={
                        'title': column[2],
                        'description': column[3],
                        'poster_url': column[4],
                        # Note: pour le lieu, on peut gérer par ID ou désignation
                        'bookable': column[6].lower() == 'true',
                        'status': column[7] if len(column) > 7 else 'published'
                    }
                )
                count += 1
            
            messages.success(request, f"{count} spectacles traités avec succès.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'importation : {str(e)}")
            
    return redirect('admin_show_index')

@user_passes_test(is_admin)
def admin_export_representations_csv(request):
    """
    Exporte la liste des représentations en format CSV.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="representations_export.csv"'
    response.write(u'\ufeff'.encode('utf8'))
    
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Spectacle', 'Date/Heure', 'Lieu', 'Places Dispos', 'Total Places'])
    
    for rep in Representation.objects.all().select_related('show', 'location'):
        writer.writerow([
            rep.id, 
            rep.show.title, 
            rep.schedule.strftime('%Y-%m-%d %H:%M:%S'), 
            rep.location.designation if rep.location else '', 
            rep.available_seats, 
            rep.total_seats
        ])
    
    return response

@user_passes_test(is_admin)
def admin_mark_notification_read(request, pk):
    """
    Marque une notification comme lue et redirige vers son lien.
    """
    from catalogue.models import Notification
    notification = get_object_or_404(Notification, pk=pk)
    notification.is_read = True
    notification.save()

    if notification.link:
        return redirect(notification.link)
    return redirect("admin_dashboard")

@user_passes_test(is_admin)
def admin_notifications(request):
    """
    Affiche la liste complète des notifications.
    """
    from catalogue.models import Notification
    from django.core.paginator import Paginator

    notifications_list = Notification.objects.all()
    paginator = Paginator(notifications_list, 20) # Show 20 notifications per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/notifications.html', {
        'page_obj': page_obj,
    })

@user_passes_test(is_admin)
def admin_mark_all_notifications_read(request):
    """
    Marque toutes les notifications non lues comme lues.
    """
    from catalogue.models import Notification
    from django.contrib import messages
    Notification.objects.filter(is_read=False).update(is_read=True)

    messages.success(request, "Toutes les notifications ont été marquées comme lues.")
    return redirect('admin_notifications')
