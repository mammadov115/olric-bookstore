from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from apps.orders.models import Order
from apps.books.models import Book
from apps.accounts.models import User
from django.db.models import Sum
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
def dashboard_revenue(request):
    """Revenue details (Partial for HTMX)"""
    active_statuses = ['confirmed', 'processing', 'shipped', 'delivered']
    orders = Order.objects.filter(status__in=active_statuses).order_by('-created_at')
    context = {'orders': orders}
    
    if request.headers.get('HX-Request'):
        return render(request, 'dashboard/partials/revenue_details.html', context)
    return render(request, 'dashboard/index.html', context)
