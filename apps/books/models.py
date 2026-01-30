from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    """
    Hierarchical category system (Self-referencing).
    Example: Fiction -> Mystery -> Noir.
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children'
    )
    image = models.ImageField(upload_to='categories/', blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

class Publisher(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='publishers/', blank=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='authors/', blank=True)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

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
    categories = models.ManyToManyField(Category, related_name='books') # 👈 Əlavə olundu
    
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

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['isbn']),
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'is_featured']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('books:book_detail', kwargs={'slug': self.slug})

    @property
    def final_price(self):
        return self.discount_price if self.discount_price else (self.price or 0)

    def is_in_stock(self):
        return self.stock > 0