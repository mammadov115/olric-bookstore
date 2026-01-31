from django.db import models

class Courier(models.Model):
    """Delivery couriers"""
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=50, blank=True)  # e.g., Motorcycle, Car, Van
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        app_label = 'orders'

    def __str__(self):
        return f"{self.name} ({self.phone})"
