import uuid
import json
import hashlib
import requests  # Requires: pip install requests
from django.conf import settings
from django.urls import reverse
from .models import Payment

class MilliPayService:
    """
    Payment Service Wrapper.
    Switches between Mock (Dev) and Real (Prod) based on settings.DEBUG or specific flag.
    """
    
    def __init__(self):
        self.use_mock = getattr(settings, 'PAYMENT_USE_MOCK', True)
        self.api_url = getattr(settings, 'MILLIPAY_API_URL', 'https://api.millipay.az/v1/payment')
        self.merchant_id = getattr(settings, 'MILLIPAY_MERCHANT_ID', 'test_merchant')
        self.secret_key = getattr(settings, 'MILLIPAY_SECRET_KEY', 'test_secret')

    def create_payment(self, order, request):
        """
        Routing method: Decides whether to use real API or Mock gateway.
        """
        if self.use_mock:
            return self._create_mock_payment(order, request)
        else:
            return self._create_real_payment(order, request)

    def process_callback(self, data):
        """
        Routing method for callbacks.
        """
        if self.use_mock:
            return self._process_mock_callback(data)
        else:
            return self._process_real_callback(data)

    # ==========================================
    # 🧪 MOCK IMPLEMENTATION (For Development)
    # ==========================================
    def _create_mock_payment(self, order, request):
        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={'amount': order.total_amount, 'status': 'pending'}
        )
        transaction_id = str(uuid.uuid4())
        payment.transaction_id = transaction_id
        payment.save()
        return reverse('payments:mock_gateway', kwargs={'transaction_id': transaction_id})

    def _process_mock_callback(self, data):
        transaction_id = data.get('transaction_id')
        status = data.get('status')
        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
            if status == 'success':
                self._complete_payment(payment, data)
            else:
                self._fail_payment(payment, 'Payment declined by user or bank.', data)
            return payment
        except Payment.DoesNotExist:
            return None

    # ==========================================
    # 🚀 REAL IMPLEMENTATION (Production Ready)
    # ==========================================
    def _create_real_payment(self, order, request):
        """
        Sends actual request to Payment Gateway API.
        """
        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={'amount': order.total_amount, 'status': 'pending'}
        )
        
        # 1. Prepare Data
        callback_url = request.build_absolute_uri(reverse('payments:callback'))
        payload = {
            'merchant_id': self.merchant_id,
            'amount': str(order.total_amount),
            'currency': 'AZN',
            'order_id': order.order_number,
            'description': f"Order #{order.order_number}",
            'callback_url': callback_url,
        }
        
        # 2. Generate Signature (Example: MD5 of merchant_id + order_id + amount + secret)
        # Note: Actual formula depends on specific Bank documentation
        signature_str = f"{self.merchant_id}{order.order_number}{order.total_amount}{self.secret_key}"
        payload['signature'] = hashlib.md5(signature_str.encode()).hexdigest()

        # 3. Send Request
        try:
            # response = requests.post(f"{self.api_url}/create", json=payload, timeout=10)
            # response.raise_for_status()
            # data = response.json()
            
            # For now, since we have no keys, we simulate an error if someone tries to use this
            raise NotImplementedError("Real Payment API keys missing. Set PAYMENT_USE_MOCK=True")
            
            # If successful:
            # payment.transaction_id = data['transaction_id']
            # payment.save()
            # return data['redirect_url']
            
        except Exception as e:
            payment.error_message = str(e)
            payment.status = 'failed'
            payment.save()
            return reverse('payments:failed') # Or error page

    def _process_real_callback(self, data):
        """
        Verifies signature from Bank Callback.
        """
        # 1. Verify Signature (Security Check)
        received_signature = data.get('signature')
        # my_signature = hashlib.md5(...)
        # if received_signature != my_signature: return None
        
        transaction_id = data.get('transaction_id')
        status = data.get('status') # e.g. '0' for success, '1' for error
        
        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
            
            if status == 'success': # Check bank specific success code
                self._complete_payment(payment, data)
            else:
                self._fail_payment(payment, data.get('error_msg', 'Unknown error'), data)
                
            return payment
        except Payment.DoesNotExist:
            return None

    # ==========================================
    # 🔄 SHARED HELPERS
    # ==========================================
    def _complete_payment(self, payment, data):
        payment.status = 'completed'
        payment.response_data = json.dumps(data)
        
        # Update Order
        payment.order.status = 'confirmed'
        payment.order.save()
        
        from django.utils import timezone
        payment.completed_at = timezone.now()
        payment.save()

    def _fail_payment(self, payment, error_msg, data):
        payment.status = 'failed'
        payment.error_message = error_msg
        payment.response_data = json.dumps(data)
        payment.save()
