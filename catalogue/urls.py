"""reservations.catalogue URL Configuration
"""
from django.urls import path
from .views import artist, type, price, locality, location, representation, review, ticket, producer_dashboard
from .views.show_ import index as show_index, show as show_detail, create as show_create, edit as show_edit, delete as show_delete
from .views.admin_dashboard import admin_show_index, admin_representation_index
from catalogue.views import press_article 


app_name='catalogue'

urlpatterns = [
    # Artist
    path('artist/', artist.index, name='artist-index'),
    path('artist/<int:artist_id>', artist.show, name='artist-show'),
    path('artist/edit/<int:artist_id>', artist.edit, name='artist-edit'),
    path('artist/create', artist.create, name='artist-create'),
    path('artist/delete/<int:artist_id>', artist.delete, name='artist-delete'),

    # Type
    path('type/', type.index, name='type-index'),
    path('type/<int:type_id>', type.show, name='type-show'),

    # Price
    path('price/', price.index, name='price-index'),
    path('price/<int:price_id>', price.show, name='price-show'),

    # Locality
    path('locality/', locality.index, name='locality-index'),
    path('locality/<int:locality_id>', locality.show, name='locality-show'),

    # Location
    path('location/', location.index, name='location-index'),
    path('location/<int:location_id>', location.show, name='location-show'),

    # Show
    path('show/', show_index, name='show-index'),
    path('show/<int:show_id>', show_detail, name='show-show'),
    path('show/create/', show_create, name='show-create'),
    path('show/edit/<int:show_id>', show_edit, name='show-edit'),
    path('show/delete/<int:show_id>', show_delete, name='show-delete'),

    # Representation
    path('representation/', representation.index, name='representation-index'),
    path('representation/<int:representation_id>', representation.show, name='representation-show'),

    # Review
    path('review/', review.index, name='review-index'),
    path('review/<int:review_id>', review.show, name='review-show'),
    path('review/create/', review.create, name='review-create'),
    path('review/edit/<int:review_id>', review.edit, name='review-edit'),
    path('review/delete/<int:review_id>', review.delete, name='review-delete'),

    # Producer Dashboard
    path('prod-dashboard/', producer_dashboard.prod_dashboard, name='prod_dashboard'),
    path('prod-dashboard/submit-show/', producer_dashboard.prod_submit_show, name='prod_submit_show'),
    path('prod-dashboard/edit-show/<int:pk>/', producer_dashboard.prod_edit_show, name='prod_edit_show'),
    path('prod-dashboard/moderate-reviews/', producer_dashboard.prod_moderate_reviews, name='prod_moderate_reviews'),
    path('prod-dashboard/pin-review/<int:review_id>/', producer_dashboard.pin_review, name='prod_pin_review'),

    # Tickets
    path('ticket/<uuid:ticket_id>', ticket.ticket_detail, name='ticket-detail'),
    path('ticket/<uuid:ticket_id>/pdf', ticket.ticket_pdf, name='ticket-pdf'),
    path('reservation/<int:reservation_id>/pdf', ticket.reservation_pdf, name='reservation-pdf'),
 
    # Section Articles de Presse
    path('press/mes-articles/', press_article.my_articles, name='my-articles'),
    path('press/rediger/', press_article.create_article, name='article-create'),
    path('press/liste/', press_article.article_list, name='article-index'),
    path('press/dashboard/', press_article.producer_dashboard, name='producer-dashboard'),
    path('press/valider/<int:article_id>/<str:action>/', press_article.validate_article, name='article-validate'),
 
 ]
