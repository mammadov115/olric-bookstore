from apps.books.models import Book
from apps.cart.models import CartItem
from .manager import CartManagerMixin
from .coupon import CouponMixin

class CartService(CartManagerMixin, CouponMixin):
    """
    Main Cart Service that composes management and coupon mixins.
    Handles basic item operations (add, remove, clear, list).
    """

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
