from django.db.models import Sum, F
from catalogue.models import RepresentationReservation, Representation

def get_show_stats(show):
    # Total tickets sold across all representations of this show
    total_sold = RepresentationReservation.objects.filter(
        representation__show=show
    ).aggregate(total=Sum('quantity'))['total'] or 0
    
    # Remaining seats across all representations
    remaining_seats = Representation.objects.filter(
        show=show
    ).aggregate(total=Sum('available_seats'))['total'] or 0
    
    return {
        'total_sold': total_sold,
        'remaining_seats': remaining_seats,
    }
