from .models import Wishlist

def wishlist_count(request):
    if request.user.is_authenticated:
        return {
            'wishlist_count': Wishlist.objects.filter(user=request.user).count(),
            'wishlist_book_ids': set(Wishlist.objects.filter(user=request.user).values_list('book_id', flat=True))
        }
    return {
        'wishlist_count': 0,
        'wishlist_book_ids': set()
    }
