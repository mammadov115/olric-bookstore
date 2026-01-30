from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order_link', 'transaction_id', 'amount', 'currency', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('transaction_id', 'order__order_number')
    readonly_fields = ('created_at', 'completed_at', 'response_data', 'error_message')
    
    def order_link(self, obj):
        return obj.order.order_number
    order_link.short_description = 'Order'
