from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from apps.orders.models import Order, Courier
from apps.books.models import Book
from apps.accounts.models import User
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

@staff_member_required
def dashboard_index(request):
    """Main dashboard entry point"""
    return render(request, 'dashboard/index.html')

@staff_member_required
def dashboard_stats(request):
    """Statistics overview (Partial for HTMX)"""
    today = timezone.now().date()
    last_30_days = today - timedelta(days=30)
    
    active_statuses = ['confirmed', 'processing', 'shipped', 'delivered']
    total_revenue = Order.objects.filter(status__in=active_statuses).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_orders = Order.objects.count()
    total_books = Book.objects.count()
    total_users = User.objects.count()
    
    recent_orders = Order.objects.order_by('-created_at')[:5]
    
    # Calculate trends
    start_date = timezone.now() - timedelta(days=30)
    revenue_30d = Order.objects.filter(
        status__in=active_statuses, 
        created_at__gte=start_date
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    new_users_30d = User.objects.filter(date_joined__gte=start_date).count()
    low_stock_count = Book.objects.filter(stock__lt=10, is_active=True).count()
    
    # Chart data (last 7 days)
    chart_labels = []
    chart_revenue = []
    for i in range(6, -1, -1):
        date = timezone.now().date() - timedelta(days=i)
        rev = Order.objects.filter(
            status__in=active_statuses,
            created_at__date=date
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        chart_labels.append(date.strftime('%d %b'))
        chart_revenue.append(float(rev))

    context = {
        'total_revenue': total_revenue,
        'revenue_30d': revenue_30d,
        'total_orders': total_orders,
        'total_books': total_books,
        'total_users': total_users,
        'new_users_30d': new_users_30d,
        'low_stock_count': low_stock_count,
        'recent_orders': recent_orders,
        'chart_labels': chart_labels,
        'chart_revenue': chart_revenue,
    }
    
    if request.headers.get('HX-Request'):
        return render(request, 'dashboard/partials/stats.html', context)
    return render(request, 'dashboard/index.html', context)

@staff_member_required
def dashboard_orders(request):
    """Orders management (Partial for HTMX)"""
    orders = Order.objects.all().order_by('-created_at')
    context = {'orders': orders}
    
    if request.headers.get('HX-Request'):
        return render(request, 'dashboard/partials/orders.html', context)
    return render(request, 'dashboard/index.html', context)

@staff_member_required
def dashboard_books(request):
    """Books management (Partial for HTMX)"""
    books = Book.objects.all().order_by('-created_at')
    low_stock_count = Book.objects.filter(stock__lt=10, is_active=True).count()
    context = {
        'books': books,
        'low_stock_count': low_stock_count
    }
    
    if request.headers.get('HX-Request'):
        return render(request, 'dashboard/partials/books.html', context)
    return render(request, 'dashboard/index.html', context)

@staff_member_required
def dashboard_users(request):
    """Users management (Partial for HTMX)"""
    users = User.objects.all().order_by('-date_joined')
    start_date = timezone.now() - timedelta(days=30)
    new_users_30d = User.objects.filter(date_joined__gte=start_date).count()
    context = {
        'users': users,
        'new_users_30d': new_users_30d
    }
    
    if request.headers.get('HX-Request'):
        return render(request, 'dashboard/partials/users.html', context)
    return render(request, 'dashboard/index.html', context)

@staff_member_required
def dashboard_revenue(request):
    """Revenue details (Partial for HTMX)"""
    active_statuses = ['confirmed', 'processing', 'shipped', 'delivered']
    orders = Order.objects.filter(status__in=active_statuses).order_by('-created_at')
    context = {'orders': orders}
    
    if request.headers.get('HX-Request'):
        return render(request, 'dashboard/partials/revenue_details.html', context)
    return render(request, 'dashboard/index.html', context)

@staff_member_required
def dashboard_order_detail(request, pk):
    """Order detailed view (Partial for HTMX)"""
    from django.shortcuts import get_object_or_404
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
    from django.shortcuts import get_object_or_404
    from django.http import HttpResponse
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
    from django.shortcuts import get_object_or_404, HttpResponse
    from apps.orders.models import Delivery
    
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

@staff_member_required
def dashboard_couriers(request):
    """Couriers management (Partial for HTMX)"""
    couriers = Courier.objects.all().order_by('-is_active', 'name')
    context = {'couriers': couriers}
    
    if request.headers.get('HX-Request'):
        return render(request, 'dashboard/partials/couriers.html', context)
    return render(request, 'dashboard/index.html', context)

@staff_member_required
@require_POST
def dashboard_add_courier(request):
    """Add new courier via HTMX"""
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    vehicle_type = request.POST.get('vehicle_type')
    
    if name and phone:
        Courier.objects.create(
            name=name,
            phone=phone,
            vehicle_type=vehicle_type
        )
    
    return dashboard_couriers(request)
