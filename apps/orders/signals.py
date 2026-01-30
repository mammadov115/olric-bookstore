from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Delivery
from .sms import SMSService

@receiver(post_save, sender=Delivery)
def send_delivery_status_sms(sender, instance, created, **kwargs):
    """
    Automatically send SMS to customer when delivery status changes
    """
    # Only send SMS if delivery has an order with a phone number
    if not instance.order or not instance.order.phone:
        return
    
    # Generate appropriate message based on status
    sms_service = SMSService()
    message = sms_service.format_order_status_message(instance.order, instance)
    
    # Send the SMS
    sms_service.send_sms(instance.order.phone, message)
