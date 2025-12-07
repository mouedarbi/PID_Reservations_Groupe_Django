from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    """
    Basic API index view
    """
    return JsonResponse({
        'message': 'Welcome to the Reservation API',
        'status': 'active'
    })
