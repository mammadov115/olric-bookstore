from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, Delivery
from .sms import SMSService

@receiver(post_save, sender=Order)
def order_status_changed_sms(sender, instance, created, **kwargs):
    """
    Send SMS when order is confirmed (paid) or updated.
    """
    # Trigger SMS on Payment Confirmation
    if not created and instance.status == 'confirmed':
        # Check if we already sent notification for this status to avoid duplicates
        # (Simple check: only send if no Delivery exists yet)
        if not hasattr(instance, 'delivery'):
            # Create automated delivery record
            Delivery.objects.create(order=instance)
            # Existing Delivery signal will pick it up and send "Order Accepted" SMS
            return

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
