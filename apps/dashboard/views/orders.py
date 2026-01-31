from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.utils import timezone
from apps.orders.models import Order, Courier, Delivery

@staff_member_required
def dashboard_orders(request):
    """Orders management (Partial for HTMX)"""
    orders = Order.objects.all().order_by('-created_at')
    context = {'orders': orders}
    
    if request.headers.get('HX-Request'):
        return render(request, 'dashboard/partials/orders.html', context)
    return render(request, 'dashboard/index.html', context)

@staff_member_required
def dashboard_order_detail(request, pk):
    """Order detailed view (Partial for HTMX)"""
    order = get_object_or_404(Order, pk=pk)
    couriers = Courier.objects.filter(is_active=True)
    has_delivery = hasattr(order, 'delivery')
    context = {'order': order, 'couriers': couriers, 'has_delivery': has_delivery}
    
    if request.headers.get('HX-Request'):
        return render(request, 'dashboard/partials/order_detail.html', context)
    return render(request, 'dashboard/index.html', context)

@staff_member_required
@require_POST
def dashboard_update_order_status(request, pk):
    """Update order status via HTMX"""
    order = get_object_or_404(Order, pk=pk)
    new_status = request.POST.get('status')
    
    if new_status in dict(Order.STATUS_CHOICES):
        order.status = new_status
        order.save()
        
        # Sync with Delivery status to ensure customer view matches admin
        if hasattr(order, 'delivery'):
            delivery = order.delivery
            
            if new_status == 'assigned':
                # Map Order 'assigned' to Delivery 'assigned'
                delivery.status = 'assigned'
                if not delivery.assigned_at:
                    delivery.assigned_at = timezone.now()
                delivery.save()
                
            elif new_status == 'picked_up':
                delivery.status = 'picked_up'
                if not delivery.picked_up_at:
                    delivery.picked_up_at = timezone.now()
                delivery.save()
                
            elif new_status == 'in_transit':
                delivery.status = 'in_transit'
                if not delivery.picked_up_at:
                    delivery.picked_up_at = timezone.now()
                delivery.save()
                
            elif new_status == 'delivered':
                delivery.status = 'delivered'
                delivery.delivered_at = timezone.now()
                if not delivery.picked_up_at:
                    delivery.picked_up_at = timezone.now()
                delivery.save()
                
            elif new_status == 'cancelled':
                delivery.status = 'failed'
                delivery.save()
                
            elif new_status == 'pending':
                delivery.status = 'pending'
                delivery.save()
        
    couriers = Courier.objects.filter(is_active=True)
    has_delivery = hasattr(order, 'delivery')
    context = {'order': order, 'couriers': couriers, 'has_delivery': has_delivery}
    return render(request, 'dashboard/partials/order_detail.html', context)

@staff_member_required
@require_POST
def dashboard_assign_courier(request, pk):
    """Assign courier to order via HTMX"""
    order = get_object_or_404(Order, pk=pk)
    
    # Check if removing courier
    try:
        if request.POST.get('remove') == 'true':
            if hasattr(order, 'delivery'):
                delivery = order.delivery
                delivery.courier = None
                delivery.status = 'pending'
                delivery.assigned_at = None
                delivery.save()
                order.refresh_from_db()
        
        # Assign new courier
        else:
            courier_id = request.POST.get('courier_id')
            if courier_id:
                courier = get_object_or_404(Courier, pk=courier_id)
                
                # Create or update delivery
                delivery, created = Delivery.objects.get_or_create(order=order)
                delivery.courier = courier
                if delivery.status == 'pending':
                    delivery.status = 'assigned'
                delivery.assigned_at = timezone.now()
                delivery.save()
                
                # Update order status if needed
                if order.status == 'confirmed':
                    order.status = 'processing'
                    order.save()
                    
        # Re-fetch order to get updated relations
        order.refresh_from_db()
        couriers = Courier.objects.filter(is_active=True)
        has_delivery = hasattr(order, 'delivery') and order.delivery.courier is not None
        
        context = {'order': order, 'couriers': couriers, 'has_delivery': has_delivery}
        return render(request, 'dashboard/partials/order_detail.html', context)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return HttpResponse(f"Error: {str(e)}", status=500)
