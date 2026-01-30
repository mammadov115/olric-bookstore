from django.contrib import admin
from django.utils import timezone
from .models import Order, OrderItem, Courier, Delivery

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['book']
    extra = 0
    readonly_fields = ('book_title', 'price', 'subtotal')
    
    def subtotal(self, obj):
        return obj.subtotal

class DeliveryInline(admin.StackedInline):
    model = Delivery
    extra = 0
    fields = ('courier', 'status', 'tracking_number', 'assigned_at', 'picked_up_at', 'delivered_at', 'notes')
    readonly_fields = ('assigned_at', 'picked_up_at', 'delivered_at')
    
    def save_model(self, request, obj, form, change):
        # Auto-update timestamps based on status
        if obj.status == 'assigned' and not obj.assigned_at:
            obj.assigned_at = timezone.now()
        elif obj.status == 'picked_up' and not obj.picked_up_at:
            obj.picked_up_at = timezone.now()
        elif obj.status == 'delivered' and not obj.delivered_at:
            obj.delivered_at = timezone.now()
        super().save_model(request, obj, form, change)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'full_name', 'total_amount', 'status', 'payment_method', 'has_delivery', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at', 'updated_at')
    search_fields = ('order_number', 'full_name', 'email', 'phone', 'user__username')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    inlines = [OrderItemInline, DeliveryInline]
    
    def has_delivery(self, obj):
        return hasattr(obj, 'delivery')
    has_delivery.boolean = True
    has_delivery.short_description = 'Tracking'
    
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

@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'vehicle_type', 'is_active', 'active_deliveries_count')
    list_filter = ('is_active', 'vehicle_type')
    search_fields = ('name', 'phone')
    
    def active_deliveries_count(self, obj):
        return obj.deliveries.exclude(status__in=['delivered', 'failed']).count()
    active_deliveries_count.short_description = 'Active Deliveries'

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('order_link', 'courier', 'status', 'tracking_number', 'assigned_at', 'delivered_at')
    list_filter = ('status', 'courier', 'created_at')
    search_fields = ('order__order_number', 'tracking_number', 'courier__name')
    readonly_fields = ('created_at', 'updated_at', 'assigned_at', 'picked_up_at', 'delivered_at')
    
    def order_link(self, obj):
        return obj.order.order_number
    order_link.short_description = 'Order'
    
    def save_model(self, request, obj, form, change):
        # Auto-update timestamps based on status
        if obj.status == 'assigned' and not obj.assigned_at:
            obj.assigned_at = timezone.now()
        elif obj.status == 'picked_up' and not obj.picked_up_at:
            obj.picked_up_at = timezone.now()
        elif obj.status == 'delivered' and not obj.delivered_at:
            obj.delivered_at = timezone.now()
            # Also update order status
            obj.order.status = 'delivered'
            obj.order.save()
        super().save_model(request, obj, form, change)
