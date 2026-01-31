from django.db import models
from apps.books.models import Book
from .cart import Cart

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    # Price at the time of adding to cart to track changes (optional but good practice)
    price_at_addition = models.DecimalField(max_digits=10, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'cart'

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"

    @property
    def subtotal(self):
        return (self.book.final_price or 0) * self.quantity
