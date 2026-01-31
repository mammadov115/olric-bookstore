from django.db import models
from django.conf import settings
from apps.coupons.models import Coupon

class Order(models.Model):
    # Order identification
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='orders'
    )
    
    # Billing/Shipping Info (Snapshot)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10, blank=True)
    
    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Coupon
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Payment and Status
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Bank Kartı'),
        ('cash', 'Nağd ödəniş'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='card')
    
    STATUS_CHOICES = [
        ('pending', 'Gözləyir'),
        ('processing', 'Hazırlanır'),
        ('assigned', 'Kuryer təyin edildi'),
        ('picked_up', 'Götürülüb'),
        ('in_transit', 'Yoldadır'),
        ('delivered', 'Çatdırılıb'),
        ('cancelled', 'Ləğv edildi'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Notes
    customer_notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        app_label = 'orders'

    def __str__(self):
        return f"Sifariş #{self.order_number}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            import datetime
            import random
            # Simple unique order number generation
            now = datetime.datetime.now()
            self.order_number = f"OLR{now.strftime('%y%m%d%H%M')}{random.randint(10, 99)}"
        super().save(*args, **kwargs)

from apps.books.models import Book

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    
    # Snapshots (Crucial for record keeping)
    book_title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price at time of purchase
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        app_label = 'orders'

    def __str__(self):
        return f"{self.quantity}x {self.book_title} for Order {self.order.order_number}"

    @property
    def subtotal(self):
        if self.price is None:
            return 0
        return self.price * self.quantity
