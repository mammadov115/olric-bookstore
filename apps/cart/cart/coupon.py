from decimal import Decimal, ROUND_HALF_UP

class CouponMixin:
    """Handles coupon logic and discount calculations."""
    
    def get_coupon(self):
        from apps.coupons.models import Coupon
        coupon_id = self.session.get('coupon_id')
        if coupon_id:
            try:
                return Coupon.objects.get(id=coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        coupon = self.get_coupon()
        if coupon:
            total = self.get_total_price()
            if coupon.min_purchase_amount and total < coupon.min_purchase_amount:
               return Decimal('0.00')
               
            if coupon.discount_type == 'fixed':
                return Decimal(str(coupon.discount_value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            else: # percentage
                discount = (Decimal(str(coupon.discount_value)) / Decimal('100')) * total
                if coupon.max_discount_amount and discount > coupon.max_discount_amount:
                     return Decimal(str(coupon.max_discount_amount)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                return discount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return Decimal('0.00')

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
