from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from apps.books.models import Book
from .models import Review
from .forms import ReviewForm

@login_required
@require_POST
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # Check if user already reviewed this book
    if Review.objects.filter(book=book, user=request.user).exists():
        return JsonResponse({
            'status': 'error',
            'message': 'Siz artıq bu kitaba rəy bildirmisiniz.'
        }, status=400)
    
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.book = book
        review.user = request.user
        review.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Rəyiniz uğurla əlavə edildi!',
            'review': {
                'user': review.user.username or review.user.email,
                'rating': review.rating,
                'comment': review.comment,
                'created_at': review.created_at.strftime('%d %b %Y'),
                'is_verified': review.is_verified_purchase
            }
        })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Rəy əlavə edilərkən xəta baş verdi.',
        'errors': form.errors
    }, status=400)

@login_required
@require_POST
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return JsonResponse({
        'status': 'success',
        'message': 'Rəyiniz silindi.'
    })

@login_required
@require_POST
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    form = ReviewForm(request.POST, instance=review)
    if form.is_valid():
        form.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Rəyiniz yeniləndi!',
            'review': {
                'rating': review.rating,
                'comment': review.comment
            }
        })
    return JsonResponse({
        'status': 'error',
        'message': 'Yeniləmə zamanı xəta baş verdi.',
        'errors': form.errors
    }, status=400)
