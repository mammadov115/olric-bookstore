from decimal import Decimal
from django.db import transaction
from .models import OrderItem

class OrderCoordinator:
    """
    Coordinates the complex logic of order creation, separating it from the View layer.
    """
    
    @staticmethod
    @transaction.atomic
    def create_order(user, order_instance, cart):
        """
        Finalizes and persists the order based on cart contents.
        
        Args:
            user: The user creating the order (can be AnonymousUser).
            order_instance: The unsaved Order model instance (from form.save(commit=False)).
            cart: The CartService instance.
            
        Returns:
            Order: The saved order instance.
        """
        
        # 1. Assign User (if authenticated)
        if user.is_authenticated:
            order_instance.user = user
            
        # 2. Calculate Pricing
        # Ensure we use Decimals for currency
        order_instance.subtotal = cart.get_total_price()
        order_instance.discount_amount = Decimal(cart.get_discount())
        order_instance.shipping_cost = Decimal(0) # Future-proof: easy to add shipping logic here later
        order_instance.total_amount = Decimal(cart.get_total_price_after_discount()) + order_instance.shipping_cost
        
        # 3. Associate Coupon
        coupon = cart.get_coupon()
        if coupon:
            order_instance.coupon = coupon
            
        # 4. Save the Order (Generate IDs)
        order_instance.save()
        
        # 5. Create Order Items (Snapshots of current price/titles)
        items_to_create = []
        for item in cart:
            items_to_create.append(OrderItem(
                order=order_instance,
                book=item.book,
                book_title=item.book.title,
                price=item.book.final_price,
                quantity=item.quantity
            ))
            
        # Bulk create is more efficient
        OrderItem.objects.bulk_create(items_to_create)
        
        # 6. Handle Side Effects (Coupons)
        if coupon:
            coupon.usage_count += 1
            coupon.save()
            
        return order_instance
