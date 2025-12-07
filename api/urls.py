from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # AUTH
    path('auth/signup/', views.PlaceholderView.as_view(), name='auth-signup'),
    path('auth/login/', views.PlaceholderView.as_view(), name='auth-login'),
    path('auth/logout/', views.PlaceholderView.as_view(), name='auth-logout'),

    # USERS
    path('users/me/', views.PlaceholderView.as_view(), name='users-me'),
    path('users/me/', views.PlaceholderView.as_view(), name='users-update-me'),
    path('users/me/roles/', views.PlaceholderView.as_view(), name='users-roles'),
    path('admin/users/<int:id>/roles/', views.PlaceholderView.as_view(), name='admin-users-roles'),
    path('users/me/subscription/', views.PlaceholderView.as_view(), name='users-subscription'),

    # ARTISTS & CATEGORIES
    path('artists/', views.PlaceholderView.as_view(), name='artists-list-create'),
    path('artists/', views.PlaceholderView.as_view(), name='artists-update'),
    path('artists/<int:id>/', views.PlaceholderView.as_view(), name='artists-detail'),
    path('types/', views.PlaceholderView.as_view(), name='types-list-create'),
    path('types/', views.PlaceholderView.as_view(), name='types-update'),
    path('types/<int:id>/', views.PlaceholderView.as_view(), name='types-detail'),
    path('artist-types/', views.PlaceholderView.as_view(), name='artist-types-list-create'),
    path('artist-types/', views.PlaceholderView.as_view(), name='artist-types-delete'),
    path('localities/', views.PlaceholderView.as_view(), name='localities-list'),
    path('localities/<int:id>/', views.PlaceholderView.as_view(), name='localities-detail'),
    path('locations/', views.PlaceholderView.as_view(), name='locations-list-create'),
    path('locations/', views.PlaceholderView.as_view(), name='locations-update'),
    path('locations/<int:id>/', views.PlaceholderView.as_view(), name='locations-detail'),

    # SHOWS
    path('shows/', views.PlaceholderView.as_view(), name='shows-list-create'),
    path('shows/', views.PlaceholderView.as_view(), name='shows-update'),
    path('shows/<int:id>/', views.PlaceholderView.as_view(), name='shows-detail'),
    path('shows/search/', views.PlaceholderView.as_view(), name='shows-search'),

    # REPRESENTATIONS
    path('representations/', views.PlaceholderView.as_view(), name='representations-list-create'),
    path('representations/', views.PlaceholderView.as_view(), name='representations-update'),
    path('representations/<int:id>/', views.PlaceholderView.as_view(), name='representations-detail'),
    path('representations/calendar/', views.PlaceholderView.as_view(), name='representations-calendar'),
    path('representations/<int:id>/availability/', views.PlaceholderView.as_view(), name='representations-availability'),

    # PRICES
    path('prices/', views.PlaceholderView.as_view(), name='prices-list-create'),
    path('prices/', views.PlaceholderView.as_view(), name='prices-update'),
    path('prices/<int:id>/', views.PlaceholderView.as_view(), name='prices-detail'),

    # CART
    path('cart/', views.PlaceholderView.as_view(), name='cart'),
    path('cart/add/', views.PlaceholderView.as_view(), name='cart-add'),
    path('cart/update/', views.PlaceholderView.as_view(), name='cart-update'),
    path('cart/remove/', views.PlaceholderView.as_view(), name='cart-remove'),

    # CHECKOUT
    path('checkout/', views.PlaceholderView.as_view(), name='checkout'),

    # RESERVATIONS
    path('reservations/', views.PlaceholderView.as_view(), name='reservations-list'),
    path('reservations/<int:id>/', views.PlaceholderView.as_view(), name='reservations-detail'),
    path('my/reservations/', views.PlaceholderView.as_view(), name='my-reservations'),

    # TICKETS
    path('reservations/<int:id>/ticket/', views.PlaceholderView.as_view(), name='reservations-ticket'),

    # REVIEWS
    path('reviews/', views.PlaceholderView.as_view(), name='reviews-list-create'),
    path('reviews/', views.PlaceholderView.as_view(), name='reviews-update'),
    path('reviews/<int:id>/', views.PlaceholderView.as_view(), name='reviews-detail'),
    path('reviews/<int:id>/validate/', views.PlaceholderView.as_view(), name='reviews-validate'),
    path('reviews/<int:id>/reject/', views.PlaceholderView.as_view(), name='reviews-reject'),

    # PRODUCER
    path('producer/shows/', views.PlaceholderView.as_view(), name='producer-shows'),
    path('producer/shows/<int:id>/stats/', views.PlaceholderView.as_view(), name='producer-shows-stats'),
    path('producer/comments/', views.PlaceholderView.as_view(), name='producer-comments'),
    path('producer/comments/<int:id>/validate/', views.PlaceholderView.as_view(), name='producer-comments-validate'),
    path('producer/comments/<int:id>/reject/', views.PlaceholderView.as_view(), name='producer-comments-reject'),
    path('producer/reviews/', views.PlaceholderView.as_view(), name='producer-reviews'),
    path('producer/reviews/<int:id>/validate/', views.PlaceholderView.as_view(), name='producer-reviews-validate'),
    path('producer/reviews/<int:id>/reject/', views.PlaceholderView.as_view(), name='producer-reviews-reject'),

    # ADMIN
    path('admin/users/', views.PlaceholderView.as_view(), name='admin-users'),
    path('admin/catalog/import/', views.PlaceholderView.as_view(), name='admin-catalog-import'),
    path('admin/catalog/export/', views.PlaceholderView.as_view(), name='admin-catalog-export'),
    path('admin/providers/shows/update/', views.PlaceholderView.as_view(), name='admin-providers-shows-update'),

    # AFFILIATE
    path('affiliate/shows/', views.PlaceholderView.as_view(), name='affiliate-shows'),
    path('affiliate/representations/', views.PlaceholderView.as_view(), name='affiliate-representations'),
    path('affiliate/subscription/', views.PlaceholderView.as_view(), name='affiliate-subscription'),

    # RSS
    path('rss/next-representations/', views.PlaceholderView.as_view(), name='rss-next-representations'),

    # PUBLIC API
    path('public/shows/', views.PlaceholderView.as_view(), name='public-shows'),
    path('public/representations/', views.PlaceholderView.as_view(), name='public-representations'),
]