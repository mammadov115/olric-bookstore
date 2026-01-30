from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Coupon
from .forms import CouponApplyForm

@require_POST
def coupon_apply(request):
    """
    Validates and applies a coupon to the session.
    """
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(
                code__iexact=code,
                valid_from__lte=timezone.now(),
                valid_until__gte=timezone.now(),
                is_active=True
            )
            
            # Check usage limits (Basic check)
            if coupon.usage_limit and coupon.usage_count >= coupon.usage_limit:
                 raise Coupon.DoesNotExist

            request.session['coupon_id'] = coupon.id
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'ok', 'message': 'Kupon tətbiq edildi!'})
                
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'Kupon yanlışdır və ya müddəti bitib.'}, status=400)

    return redirect('cart:cart_detail')
