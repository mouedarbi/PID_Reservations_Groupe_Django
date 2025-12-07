from django.urls import path
from .views import auth, users, artists, types, artist_types, localities, locations, shows, representations, prices, cart, checkout, reservations, tickets, reviews, producer, admin_api, affiliate, rss, public_api

app_name = 'api'

urlpatterns = [
    # AUTH
    path('auth/signup/', auth.AuthSignupView.as_view(), name='auth-signup'),
    path('auth/login/', auth.AuthLoginView.as_view(), name='auth-login'),
    path('auth/logout/', auth.AuthLogoutView.as_view(), name='auth-logout'),

    # USERS
    path('users/me/', users.UsersMeView.as_view(), name='users-me'),
    path('users/me/', users.UsersMeView.as_view(), name='users-update-me'),
    path('users/me/roles/', users.UsersRolesView.as_view(), name='users-roles'),
    path('admin/users/<int:id>/roles/', users.AdminUsersRolesView.as_view(), name='admin-users-roles'),
    path('users/me/subscription/', users.UsersSubscriptionView.as_view(), name='users-subscription'),

    # ARTISTS & CATEGORIES
    path('artists/', artists.ArtistsView.as_view(), name='artists-list-create'),
    path('artists/', artists.ArtistsView.as_view(), name='artists-update'),
    path('artists/<int:id>/', artists.ArtistsDetailView.as_view(), name='artists-detail'),
    path('types/', types.TypesView.as_view(), name='types-list-create'),
    path('types/', types.TypesView.as_view(), name='types-update'),
    path('types/<int:id>/', types.TypesDetailView.as_view(), name='types-detail'),
    path('artist-types/', artist_types.ArtistTypesView.as_view(), name='artist-types-list-create'),
    path('artist-types/', artist_types.ArtistTypesView.as_view(), name='artist-types-delete'),
    path('localities/', localities.LocalitiesView.as_view(), name='localities-list'),
    path('localities/<int:id>/', localities.LocalitiesDetailView.as_view(), name='localities-detail'),
    path('locations/', locations.LocationsView.as_view(), name='locations-list-create'),
    path('locations/', locations.LocationsView.as_view(), name='locations-update'),
    path('locations/<int:id>/', locations.LocationsDetailView.as_view(), name='locations-detail'),

    # SHOWS
    path('shows/', shows.ShowsView.as_view(), name='shows-list-create'),
    path('shows/', shows.ShowsView.as_view(), name='shows-update'),
    path('shows/<int:id>/', shows.ShowsDetailView.as_view(), name='shows-detail'),
    path('shows/search/', shows.ShowsSearchView.as_view(), name='shows-search'),

    # REPRESENTATIONS
    path('representations/', representations.RepresentationsView.as_view(), name='representations-list-create'),
    path('representations/', representations.RepresentationsView.as_view(), name='representations-update'),
    path('representations/<int:id>/', representations.RepresentationsDetailView.as_view(), name='representations-detail'),
    path('representations/calendar/', representations.RepresentationsCalendarView.as_view(), name='representations-calendar'),
    path('representations/<int:id>/availability/', representations.RepresentationsAvailabilityView.as_view(), name='representations-availability'),

    # PRICES
    path('prices/', prices.PricesView.as_view(), name='prices-list-create'),
    path('prices/', prices.PricesView.as_view(), name='prices-update'),
    path('prices/<int:id>/', prices.PricesDetailView.as_view(), name='prices-detail'),

    # CART
    path('cart/', cart.CartView.as_view(), name='cart'),
    path('cart/add/', cart.CartAddView.as_view(), name='cart-add'),
    path('cart/update/', cart.CartUpdateView.as_view(), name='cart-update'),
    path('cart/remove/', cart.CartRemoveView.as_view(), name='cart-remove'),

    # CHECKOUT
    path('checkout/', checkout.CheckoutView.as_view(), name='checkout'),

    # RESERVATIONS
    path('reservations/', reservations.ReservationsView.as_view(), name='reservations-list'),
    path('reservations/<int:id>/', reservations.ReservationsDetailView.as_view(), name='reservations-detail'),
    path('my/reservations/', reservations.MyReservationsView.as_view(), name='my-reservations'),

    # TICKETS
    path('reservations/<int:id>/ticket/', tickets.TicketsView.as_view(), name='reservations-ticket'),

    # REVIEWS
    path('reviews/', reviews.ReviewsView.as_view(), name='reviews-list-create'),
    path('reviews/', reviews.ReviewsView.as_view(), name='reviews-update'),
    path('reviews/<int:id>/', reviews.ReviewsDetailView.as_view(), name='reviews-detail'),
    path('reviews/<int:id>/validate/', reviews.ReviewsValidateView.as_view(), name='reviews-validate'),
    path('reviews/<int:id>/reject/', reviews.ReviewsRejectView.as_view(), name='reviews-reject'),

    # PRODUCER
    path('producer/shows/', producer.ProducerShowsView.as_view(), name='producer-shows'),
    path('producer/shows/<int:id>/stats/', producer.ProducerShowsStatsView.as_view(), name='producer-shows-stats'),
    path('producer/comments/', producer.ProducerCommentsView.as_view(), name='producer-comments'),
    path('producer/comments/<int:id>/validate/', producer.ProducerCommentsValidateView.as_view(), name='producer-comments-validate'),
    path('producer/comments/<int:id>/reject/', producer.ProducerCommentsRejectView.as_view(), name='producer-comments-reject'),
    path('producer/reviews/', producer.ProducerReviewsView.as_view(), name='producer-reviews'),
    path('producer/reviews/<int:id>/validate/', producer.ProducerReviewsValidateView.as_view(), name='producer-reviews-validate'),
    path('producer/reviews/<int:id>/reject/', producer.ProducerReviewsRejectView.as_view(), name='producer-reviews-reject'),

    # ADMIN
    path('admin/users/', admin_api.AdminApiUsersView.as_view(), name='admin-users'),
    path('admin/catalog/import/', admin_api.AdminCatalogImportView.as_view(), name='admin-catalog-import'),
    path('admin/catalog/export/', admin_api.AdminCatalogExportView.as_view(), name='admin-catalog-export'),
    path('admin/providers/shows/update/', admin_api.AdminProvidersShowsUpdateView.as_view(), name='admin-providers-shows-update'),

    # AFFILIATE
    path('affiliate/shows/', affiliate.AffiliateShowsView.as_view(), name='affiliate-shows'),
    path('affiliate/representations/', affiliate.AffiliateRepresentationsView.as_view(), name='affiliate-representations'),
    path('affiliate/subscription/', affiliate.AffiliateSubscriptionView.as_view(), name='affiliate-subscription'),

    # RSS
    path('rss/next-representations/', rss.RssNextRepresentationsView.as_view(), name='rss-next-representations'),

    # PUBLIC API
    path('public/shows/', public_api.PublicShowsView.as_view(), name='public-shows'),
    path('public/representations/', public_api.PublicRepresentationsView.as_view(), name='public-representations'),
]