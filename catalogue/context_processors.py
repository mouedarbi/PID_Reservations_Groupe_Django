from catalogue.models import Notification

def admin_notifications(request):
    if request.user.is_authenticated and request.user.is_staff:
        notifications = Notification.objects.filter(is_read=False).order_by('-created_at')[:10]
        unread_count = Notification.objects.filter(is_read=False).count()
        return {
            'admin_notifications': notifications,
            'unread_notifications_count': unread_count
        }
    return {}
