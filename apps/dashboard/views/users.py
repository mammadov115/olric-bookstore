from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from apps.accounts.models import User
from django.utils import timezone
from datetime import timedelta

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
