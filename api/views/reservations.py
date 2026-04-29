from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from catalogue.models.reservation import Reservation
from api.serializers.reservations import ReservationSerializer

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to access it.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        return obj.user == request.user

class ReservationsView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Admin sees all, regular users see nothing (or should use MyReservationsView)
        # To be strict:
        if self.request.user.is_staff:
            return Reservation.objects.all()
        return Reservation.objects.none() # Or raise PermissionDenied

    def perform_create(self, serializer):
        # Auto-assign user
        serializer.save(user=self.request.user, status="Confirmed")

class ReservationsDetailView(generics.RetrieveDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    lookup_field = 'id'

    def perform_destroy(self, instance):
        # Restore seats
        representation = instance.representation
        representation.available_seats += instance.quantity
        representation.save()
        instance.delete()

class MyReservationsView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)
