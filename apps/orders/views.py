from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.cart.cart import CartService
from .models import Order, OrderItem
from .forms import OrderCreateForm

def order_create(request):
    cart = CartService(request)
    if cart.get_total_items() == 0:
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            
            # Pricing logic
            from decimal import Decimal
            order.subtotal = cart.get_total_price()
            order.discount_amount = Decimal(cart.get_discount())
            order.shipping_cost = Decimal(0) # For now, can include shipping logic later
            order.total_amount = Decimal(cart.get_total_price_after_discount()) + order.shipping_cost
            
            # Associate Coupon
            coupon = cart.get_coupon()
            if coupon:
                order.coupon = coupon
            
            order.save()

            # Create Order Items (Snapshots)
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    book=item.book,
                    book_title=item.book.title,
                    price=item.book.final_price,
                    quantity=item.quantity
                )
            
            # Increment coupon usage AFTER order is saved
            if coupon:
                coupon.usage_count += 1
                coupon.save()
            
            # Clear the cart and coupon session after order is complete
            cart.clear()
            request.session.pop('coupon_id', None)
            
            if order.payment_method == 'card':
                return redirect('payments:process', order_number=order.order_number)
            
            return render(request, 'orders/order_success.html', {'order': order})
    else:
        # Pre-fill with user info if authenticated
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'full_name': f"{request.user.first_name} {request.user.last_name}".strip(),
                'email': request.user.email,
            }
        form = OrderCreateForm(initial=initial_data)

    return render(request, 'orders/order_create.html', {
        'cart': cart, 
        'form': form
    })

@login_required
def order_list(request):
    orders = request.user.orders.all()
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

def order_track(request, order_number):
    """
    Public tracking page for customers to check delivery status
    """
    order = get_object_or_404(Order, order_number=order_number)
    
    # Define all possible statuses with display info
    tracking_stages = [
        {'key': 'pending', 'label': 'Gözləyir', 'icon': 'clock'},
        {'key': 'assigned', 'label': 'Kuryer təyin edilib', 'icon': 'user-check'},
        {'key': 'picked_up', 'label': 'Götürülüb', 'icon': 'box'},
        {'key': 'in_transit', 'label': 'Yoldadır', 'icon': 'truck'},
        {'key': 'delivered', 'label': 'Çatdırılıb', 'icon': 'check-circle'},
    ]
    
    # Get current delivery status
    current_status = None
    delivery = None
    if hasattr(order, 'delivery'):
        delivery = order.delivery
        current_status = delivery.status
    
    # Mark stages as complete based on current status
    status_order = ['pending', 'assigned', 'picked_up', 'in_transit', 'delivered']
    current_index = status_order.index(current_status) if current_status in status_order else -1
    
    for i, stage in enumerate(tracking_stages):
        stage['is_complete'] = i <= current_index
        stage['is_current'] = i == current_index
    
    context = {
        'order': order,
        'delivery': delivery,
        'tracking_stages': tracking_stages,
        'current_status': current_status,
    }
    
    return render(request, 'orders/order_track.html', context)

