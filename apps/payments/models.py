from django.db import models
from apps.orders.models import Order

class Payment(models.Model):
    """Payment transactions"""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    
    # MilliÖn/Gateway info
    transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    gateway_order_id = models.CharField(max_length=100, blank=True)
    
    # Amount
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='AZN')
    
    # Payment Details
    payment_method = models.CharField(max_length=50, default='credit_card')
    
    # Status
    STATUS_CHOICES = [
        ('pending', 'Gözləyir'),
        ('processing', 'İşlənir'),
        ('completed', 'Tamamlandı'),
        ('failed', 'Uğursuz'),
        ('refunded', 'Geri qaytarıldı'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Response data (JSON)
    response_data = models.TextField(blank=True, default='{}')
    error_message = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.order_number}"
