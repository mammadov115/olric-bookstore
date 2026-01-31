from django.db import models
from django.db.models import Avg, Count, Q

class BookManager(models.Manager):
    def get_queryset(self):
        # We override get_queryset to ensure 'is_active' filter is not applied globally by default unless desired.
        # But typically managers just return the base queryset.
        # Here we just return the default queryset.
        return super().get_queryset()

    def with_stats(self):
        """
        Annotates the queryset with average rating and review count.
        Using this prevents N+1 queries when accessing avg_rating and review_count.
        """
        return self.annotate(
            _avg_rating=Avg('reviews__rating', filter=Q(reviews__is_active=True)),
            _review_count=Count('reviews', filter=Q(reviews__is_active=True))
        )
