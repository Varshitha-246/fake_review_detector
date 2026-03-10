from .models import ContactMessage

def notification_context(request):
    unread_count = 0
    admin_unread = 0

    if request.user.is_authenticated:

        # User unread replies count
        unread_count = ContactMessage.objects.filter(
            email=request.user.email,
            is_replied=True,
            is_read=False
        ).count()

        # Admin unread messages count
        if request.user.is_superuser:
            admin_unread = ContactMessage.objects.filter(
                is_replied=False
            ).count()

    return {
        "unread_count": unread_count,
        "admin_unread": admin_unread
    }

