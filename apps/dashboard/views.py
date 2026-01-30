from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from apps.orders.models import Order
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
    
    # Chart data (last 7 days)
    chart_data = []
    for i in range(6, -1, -1):
        date = timezone.now().date() - timedelta(days=i)
        rev = Order.objects.filter(
            status__in=active_statuses,
            created_at__date=date
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        chart_data.append({
            'date': date.strftime('%d %b'),
            'revenue': float(rev)
        })

    # Find max revenue for scaling chart
    max_rev = max([d['revenue'] for d in chart_data]) or 1
    for d in chart_data:
        d['height'] = (d['revenue'] / max_rev) * 100

    context = {
        'total_revenue': total_revenue,
        'revenue_30d': revenue_30d,
        'total_orders': total_orders,
        'total_books': total_books,
        'total_users': total_users,
        'new_users_30d': new_users_30d,
        'recent_orders': recent_orders,
        'chart_data': chart_data,
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
    context = {'books': books}
    
    if request.headers.get('HX-Request'):
        return render(request, 'dashboard/partials/books.html', context)
    return render(request, 'dashboard/index.html', context)

@staff_member_required
def dashboard_users(request):
    """Users management (Partial for HTMX)"""
    users = User.objects.all().order_by('-date_joined')
    context = {'users': users}
    
    if request.headers.get('HX-Request'):
        return render(request, 'dashboard/partials/users.html', context)
    return render(request, 'dashboard/index.html', context)
