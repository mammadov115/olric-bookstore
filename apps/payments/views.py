from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from apps.orders.models import Order
from .models import Payment
from .services import MilliPayService

def payment_process(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    
    if order.status != 'pending':
        return redirect('orders:order_detail', order_number=order.order_number)

    # Initiate payment
    service = MilliPayService()
    payment_url = service.create_payment(order, request)
    
    return redirect(payment_url)

def mock_gateway(request, transaction_id):
    """
    Simulates the external bank page.
    """
    payment = get_object_or_404(Payment, transaction_id=transaction_id)
    return render(request, 'payments/mock_gateway.html', {'payment': payment})

def payment_callback(request):
    """
    Handle the return from the bank.
    """
    transaction_id = request.GET.get('transaction_id')
    result = request.GET.get('result') # 'success' or 'fail'
    
    service = MilliPayService()
    payment = service.process_callback({
        'transaction_id': transaction_id,
        'status': result
    })
    
    if payment and payment.status == 'completed':
        return render(request, 'payments/success.html', {'order': payment.order})
    else:
        return render(request, 'payments/failed.html', {'payment': payment})
