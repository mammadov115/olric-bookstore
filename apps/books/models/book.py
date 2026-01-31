from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from ..managers import BookManager
from .category import Category
from .publisher import Publisher
from .author import Author

class Book(models.Model):
    class Format(models.TextChoices):
        HARDCOVER = 'hardcover', _('Hardcover')
        PAPERBACK = 'paperback', _('Paperback')
        EBOOK = 'ebook', _('E-book')

    # Basic Info
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, unique=True)
    subtitle = models.CharField(max_length=500, blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    description = models.TextField()
    
    # Relationships
    authors = models.ManyToManyField(Author, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, related_name='books')
    categories = models.ManyToManyField(Category, related_name='books')
    
    # Metadata
    publication_date = models.DateField(null=True, blank=True)
    language = models.CharField(max_length=10, default='az')
    pages = models.PositiveIntegerField(null=True, blank=True)
    format = models.CharField(max_length=20, choices=Format.choices, default=Format.PAPERBACK)
    cover_image = models.ImageField(upload_to='books/covers/')
    
    # Pricing & Stock
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(default=0)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    
    # Analytics
    views_count = models.PositiveIntegerField(default=0)
    sales_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BookManager()

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['isbn']),
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'is_featured']),
        ]
        app_label = 'books'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('books:book_detail', kwargs={'slug': self.slug})

    @property
    def final_price(self):
        return self.discount_price if self.discount_price else (self.price or 0)

    @property
    def avg_rating(self):
        if hasattr(self, '_avg_rating') and self._avg_rating is not None:
            return round(self._avg_rating, 1)
            
        from apps.reviews.models import Review
        reviews = Review.objects.filter(book=self, is_active=True)
        if reviews.exists():
            from django.db.models import Avg
            avg = reviews.aggregate(Avg('rating'))['rating__avg']
            return round(avg, 1) if avg else 0
        return 0

    @property
    def review_count(self):
        if hasattr(self, '_review_count'):
            return self._review_count
            
        from apps.reviews.models import Review
        return Review.objects.filter(book=self, is_active=True).count()

    def is_in_stock(self):
        return self.stock > 0
