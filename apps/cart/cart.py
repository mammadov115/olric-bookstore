from django.conf import settings
from apps.books.models import Book
from .models import Cart, CartItem

class CartService:
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

    def add(self, book_id, quantity=1, update_quantity=False):
        book = Book.objects.get(id=book_id)
        item, created = CartItem.objects.get_or_create(
            cart=self.cart,
            book=book,
            defaults={'quantity': quantity, 'price_at_addition': book.final_price}
        )
        
        if not created:
            if update_quantity:
                item.quantity = quantity
            else:
                item.quantity += quantity
            item.save()
        return item

    def remove(self, book_id):
        CartItem.objects.filter(cart=self.cart, book_id=book_id).delete()

    def clear(self):
        self.cart.items.all().delete()

    def get_total_price(self):
        return self.cart.total_price

    def get_total_items(self):
        return self.cart.total_items
    
    def __len__(self):
        return self.get_total_items()

    def __iter__(self):
        return iter(self.cart.items.all())
