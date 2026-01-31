from django.shortcuts import render
from apps.cart.cart import CartService

def cart_detail(request):
    cart = CartService(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})
