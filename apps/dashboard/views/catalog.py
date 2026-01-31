from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from apps.books.models import Book

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
