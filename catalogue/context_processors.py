from catalogue.models import Notification, Show

def admin_notifications(request):
    if request.user.is_authenticated and request.user.is_staff:
        # Notifications de la cloche (bell)
        notifications = Notification.objects.filter(is_read=False).order_by('-created_at')[:10]
        unread_count = Notification.objects.filter(is_read=False).count()
        
        # Compteur pour la sidebar (Approbation Spectacles)
        pending_shows_count = Show.objects.filter(status='pending').count()
        
        return {
            'admin_notifications': notifications,
            'unread_notifications_count': unread_count,
            'pending_shows_count': pending_shows_count
        }
    return {}
