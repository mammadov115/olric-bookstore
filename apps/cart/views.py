from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from apps.books.models import Book
from .cart import CartService

def cart_detail(request):
    cart = CartService(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

@require_POST
def cart_add(request, book_id):
    cart = CartService(request)
    book = get_object_or_404(Book, id=book_id)
    quantity = int(request.POST.get('quantity', 1))
    
    cart.add(book_id=book_id, quantity=quantity)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        from django.template.loader import render_to_string
        mini_cart_html = render_to_string('cart/includes/mini_cart.html', {'cart': cart}, request=request)
        return JsonResponse({
            'status': 'success',
            'total_items': cart.get_total_items(),
            'message': f'"{book.title}" səbətə əlavə edildi.',
            'mini_cart_html': mini_cart_html
        })
    
    return redirect('cart:cart_detail')

@require_POST
def cart_update(request, book_id):
    cart = CartService(request)
    quantity = int(request.POST.get('quantity'))
    
    item = cart.add(book_id=book_id, quantity=quantity, update_quantity=True)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'item_subtotal': item.subtotal,
            'cart_total': cart.get_total_price(),
            'total_items': cart.get_total_items()
        })
    
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, book_id):
    cart = CartService(request)
    cart.remove(book_id)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'cart_total': cart.get_total_price(),
            'total_items': cart.get_total_items()
        })
    
    return redirect('cart:cart_detail')
