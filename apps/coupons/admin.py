from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Coupon, CouponUsage

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'valid_from', 'valid_until', 'usage_limit', 'usage_count', 'is_active')
    list_filter = ('is_active', 'discount_type', 'valid_from', 'valid_until')
    search_fields = ('code', 'description')
    readonly_fields = ('usage_count', 'view_usage_history')
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('code', 'description', 'is_active')
        }),
        ('Discount Settings', {
            'fields': ('discount_type', 'discount_value')
        }),
        ('Conditions', {
            'fields': ('min_purchase_amount', 'max_discount_amount')
        }),
        ('Usage Limits', {
            'fields': ('usage_limit', 'usage_limit_per_user', 'usage_count', 'view_usage_history')
        }),
        ('Validity Period', {
            'fields': ('valid_from', 'valid_until')
        }),
    )
    
    def view_usage_history(self, obj):
        if obj.pk:
            url = reverse('admin:coupons_couponusage_changelist') + f'?coupon__id__exact={obj.pk}'
            count = obj.usages.count()
            return format_html('<a href="{}">{} usage(s) - View Details</a>', url, count)
        return '-'
    view_usage_history.short_description = 'Usage History'

@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ('coupon', 'user', 'order', 'discount_amount', 'used_at')
    list_filter = ('used_at',)
    search_fields = ('coupon__code', 'user__username', 'order__order_number')
    readonly_fields = ('coupon', 'user', 'order', 'discount_amount', 'used_at')
    
    def has_add_permission(self, request):
        # Usage records should only be created by the system, not manually
        return False
