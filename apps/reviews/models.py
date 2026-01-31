from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from apps.books.models import Book

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_("Rating")
    )
    comment = models.TextField(verbose_name=_("Comment"))
    is_verified_purchase = models.BooleanField(default=False, verbose_name=_("Verified Purchase"))
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('book', 'user') # One review per book per user
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self):
        return f"{self.user.username or self.user.email}'s review for {self.book.title}"

    def save(self, *args, **kwargs):
        # Auto-check for verified purchase if not already set
        if not self.is_verified_purchase:
            from apps.orders.models import OrderItem
            verified = OrderItem.objects.filter(
                order__user=self.user,
                book=self.book,
                order__status='delivered' # Assuming 'delivered' means verified
            ).exists()
            self.is_verified_purchase = verified
        super().save(*args, **kwargs)
