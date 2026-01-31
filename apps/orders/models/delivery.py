from django.db import models
from .order import Order
from .courier import Courier

class Delivery(models.Model):
    """Delivery tracking for orders"""
    STATUS_CHOICES = [
        ('pending', 'Gözləyir'),
        ('assigned', 'Kuryerə təyin edilib'),
        ('picked_up', 'Götürülüb'),
        ('in_transit', 'Yoldadır'),
        ('delivered', 'Çatdırılıb'),
        ('failed', 'Uğursuz'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery')
    courier = models.ForeignKey(Courier, on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Timestamps
    assigned_at = models.DateTimeField(null=True, blank=True)
    picked_up_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    # Tracking notes
    notes = models.TextField(blank=True)
    tracking_number = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Deliveries'
        app_label = 'orders'

    def __str__(self):
        return f"Delivery for {self.order.order_number} - {self.get_status_display()}"
