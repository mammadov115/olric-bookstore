from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from apps.books.models import Book
from .models import Wishlist
from django.db import IntegrityError

@login_required
@require_POST
def toggle_wishlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, book=book)
    
    if wishlist_item.exists():
        wishlist_item.delete()
        added = False
        message = "Kitab istək siyahısından çıxarıldı."
    else:
        try:
            Wishlist.objects.create(user=request.user, book=book)
            added = True
            message = "Kitab istək siyahısına əlavə edildi."
        except IntegrityError:
            added = True
            message = "Kitab artıq siyahıdadır."
            
    return JsonResponse({
        'status': 'success',
        'added': added,
        'message': message,
        'wishlist_count': Wishlist.objects.filter(user=request.user).count()
    })

@login_required
def wishlist_list(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('book').prefetch_related('book__authors', 'book__categories')
    return render(request, 'wishlist/wishlist_list.html', {
        'wishlist_items': wishlist_items
    })
