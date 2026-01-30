from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['book']
    extra = 0
    readonly_fields = ('book_title', 'price', 'subtotal')
    
    def subtotal(self, obj):
        return obj.subtotal

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'full_name', 'total_amount', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at', 'updated_at')
    search_fields = ('order_number', 'full_name', 'email', 'phone', 'user__username')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Identification', {
            'fields': ('order_number', 'user', 'status', 'created_at')
        }),
        ('Customer Info', {
            'fields': ('full_name', 'email', 'phone', 'customer_notes')
        }),
        ('Shipping Address', {
            'fields': ('address', 'city', 'postal_code')
        }),
        ('Financials', {
            'fields': ('payment_method', 'subtotal', 'shipping_cost', 'discount_amount', 'total_amount', 'coupon')
        }),
    )
