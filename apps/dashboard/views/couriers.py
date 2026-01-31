from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from apps.orders.models import Courier

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
