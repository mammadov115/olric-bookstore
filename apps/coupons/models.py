from django.db import models
from django.conf import settings

class Coupon(models.Model):
    """Discount coupons"""
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    # Discount
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Faiz'),
        ('fixed', 'Sabit məbləğ'),
    ]
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Conditions
    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Usage limits
    usage_limit = models.IntegerField(null=True, blank=True)  # Total uses
    usage_limit_per_user = models.IntegerField(default=1)
    usage_count = models.IntegerField(default=0)
    
    # Validity
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    
    # Status
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.code

class CouponUsage(models.Model):
    """Track coupon usage"""
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='usages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='coupon_usages', null=True, blank=True)
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='coupon_usages', null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    used_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-used_at']
