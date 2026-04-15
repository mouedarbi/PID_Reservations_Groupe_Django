from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'reservation', 'amount', 'currency', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('stripe_session_id', 'reservation__id', 'stripe_payment_intent_id')
    readonly_fields = ('stripe_session_id', 'stripe_payment_intent_id', 'created_at', 'reservation')
