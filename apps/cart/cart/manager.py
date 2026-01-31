from django.conf import settings
from apps.cart.models import Cart, CartItem

class CartManagerMixin:
    """Manages creation, retrieval, and merging of carts."""
    
    def __init__(self, request):
        self.session = request.session
        self.request = request
        self.cart = self._get_or_create_cart()

    def _get_or_create_cart(self):
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            # If there's an anonymous cart in session, merge it
            session_cart_id = self.session.get(settings.CART_SESSION_ID)
            if session_cart_id:
                try:
                    anon_cart = Cart.objects.get(id=session_cart_id, user__isnull=True)
                    self._merge_carts(cart, anon_cart)
                    self.session.pop(settings.CART_SESSION_ID)
                except Cart.DoesNotExist:
                    pass
            return cart
        else:
            cart_id = self.session.get(settings.CART_SESSION_ID)
            if cart_id:
                try:
                    return Cart.objects.get(id=cart_id, user__isnull=True)
                except Cart.DoesNotExist:
                    pass
            
            # Create new anonymous cart
            cart = Cart.objects.create(session_key=self.session.session_key)
            self.session[settings.CART_SESSION_ID] = cart.id
            return cart

    def _merge_carts(self, user_cart, anon_cart):
        for item in anon_cart.items.all():
            user_item, created = CartItem.objects.get_or_create(
                cart=user_cart,
                book=item.book,
                defaults={'quantity': item.quantity, 'price_at_addition': item.price_at_addition}
            )
            if not created:
                user_item.quantity += item.quantity
                user_item.save()
        anon_cart.delete()
