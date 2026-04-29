from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status, permissions

from catalogue.models.reservation import Reservation

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to view it.
    """
    def has_object_permission(self, request, view, obj):
        # Admins can access any ticket
        if request.user.is_staff:
            return True
        # The user who made the reservation can access their own ticket
        return obj.user == request.user

class TicketsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get(self, request, pk, *args, **kwargs):
        try:
            reservation = Reservation.objects.select_related('representation__show', 'representation__location').get(pk=pk)
        except Reservation.DoesNotExist:
            return HttpResponse("Réservation non trouvée.", status=status.HTTP_404_NOT_FOUND)
        
        # Check object permissions
        self.check_object_permission(request, reservation)

        # Generate a simple HTML ticket
        html = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Votre Billet</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; border: 2px solid black; padding: 20px; }}
                h1 {{ color: #333; }}
                .ticket-info {{ margin-top: 20px; }}
                .ticket-info p {{ margin: 5px 0; }}
            </style>
        </head>
        <body>
            <h1>Billet pour votre réservation</h1>
            <div class="ticket-info">
                <p><strong>Spectacle:</strong> {reservation.representation.show.title}</p>
                <p><strong>Lieu:</strong> {reservation.representation.location.designation}</p>
                <p><strong>Date et Heure:</strong> {reservation.representation.when.strftime('%d/%m/%Y à %Hh%M')}</p>
                <p><strong>Quantité:</strong> {reservation.quantity}</p>
                <p><strong>Réservé par:</strong> {reservation.user.first_name} {reservation.user.last_name}</p>
                <p><strong>Numéro de réservation:</strong> {reservation.id}</p>
            </div>
            <hr>
            <p><em>Veuillez présenter ce billet à l'entrée.</em></p>
        </body>
        </html>
        """
        
        return HttpResponse(html, content_type='text/html; charset=utf-8', status=status.HTTP_200_OK)