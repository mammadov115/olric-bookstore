from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class SMSService:
    """
    SMS Service Wrapper.
    Switches between Mock (Dev) and Real (Prod) based on settings.
    """
    
    def __init__(self):
        self.use_mock = getattr(settings, 'SMS_USE_MOCK', True)
        self.api_url = getattr(settings, 'SMS_API_URL', 'https://sms.az/api/send')
        self.api_key = getattr(settings, 'SMS_API_KEY', 'test_key')
        self.sender_name = getattr(settings, 'SMS_SENDER_NAME', 'OLRIC')

    def send_sms(self, phone, message):
        """
        Routing method: Decides whether to use real SMS API or Mock.
        """
        if self.use_mock:
            return self._send_mock_sms(phone, message)
        else:
            return self._send_real_sms(phone, message)

    # ==========================================
    # 🧪 MOCK IMPLEMENTATION (For Development)
    # ==========================================
    def _send_mock_sms(self, phone, message):
        """Simulates sending SMS by logging to console"""
        logger.info(f"📱 [MOCK SMS] To: {phone}")
        logger.info(f"📝 [MOCK SMS] Message: {message}")
        print(f"\n{'='*60}")
        print(f"📱 SMS SENT (MOCK)")
        print(f"{'='*60}")
        print(f"To: {phone}")
        print(f"From: {self.sender_name}")
        print(f"Message: {message}")
        print(f"{'='*60}\n")
        return {'status': 'success', 'mock': True}

    # ==========================================
    # 🚀 REAL IMPLEMENTATION (Production Ready)
    # ==========================================
    def _send_real_sms(self, phone, message):
        """
        Sends actual SMS via provider API.
        Replace with your SMS provider's implementation (e.g., Twilio, SMS.az, etc.)
        """
        import requests
        
        try:
            # Example implementation - adjust based on your SMS provider
            payload = {
                'api_key': self.api_key,
                'sender': self.sender_name,
                'phone': phone,
                'message': message
            }
            
            # Uncomment when you have real API credentials:
            # response = requests.post(self.api_url, json=payload, timeout=10)
            # response.raise_for_status()
            # return response.json()
            
            # For now, raise error if someone tries to use real SMS without setup
            raise NotImplementedError("Real SMS API not configured. Set SMS_USE_MOCK=True")
            
        except Exception as e:
            logger.error(f"SMS sending failed: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    # ==========================================
    # 📧 MESSAGE TEMPLATES
    # ==========================================
    @staticmethod
    def format_order_status_message(order, delivery):
        """Generate SMS message based on delivery status"""
        messages = {
            'pending': f"Salam! #{order.order_number} sifarişiniz qəbul edildi. Tezliklə kuryer təyin ediləcək.",
            'assigned': f"Kuryer təyin edildi! {delivery.courier.name} ({delivery.courier.phone}) sifarişi çatdıracaq.",
            'picked_up': f"Sifarişiniz kuryer tərəfindən götürülüb və yola çıxıb.",
            'in_transit': f"Sifarişiniz yoldadır. Tezliklə çatdırılacaq.",
            'delivered': f"Sifarişiniz çatdırılıb! Olric Bookstore'u seçdiyiniz üçün təşəkkür edirik! 📚",
            'failed': f"Çatdırılma zamanı problem yarandı. Zəhmət olmasa bizimlə əlaqə saxlayın."
        }
        return messages.get(delivery.status, f"Sifarişiniz statusu: {delivery.get_status_display()}")
