# 📏 Coding Rules & Standards - Olric Bookstore

## 📋 Ümumi Baxış

Bu sənəd Olric Bookstore layihəsində istifadə olunan kodlaşdırma standartları, naming conventions, best practices və code review qaydalarını müəyyən edir.

---

## 🎯 Ümumi Prinsiplər

### **1. DRY (Don't Repeat Yourself)**
- ✅ Təkrarlanan kodu funksiya/class-a çevir
- ✅ Reusable components yarat
- ✅ Template inheritance istifadə et

### **2. KISS (Keep It Simple, Stupid)**
- ✅ Sadə həllər üstünlük təşkil edir
- ✅ Over-engineering-dən qaçın
- ✅ Readable code > Clever code

### **3. YAGNI (You Aren't Gonna Need It)**
- ✅ Yalnız lazım olan funksionallığı implement et
- ✅ Future-proofing-dən qaçın
- ✅ Refactor when needed, not before

### **4. Separation of Concerns**
- ✅ Hər bir modul öz məsuliyyətinə cavabdehdir
- ✅ Business logic views-də, presentation templates-də
- ✅ Fat models, thin views

---

## 🐍 Python Coding Standards

### **PEP 8 Compliance**

Bütün Python kodu **PEP 8** standartlarına uyğun olmalıdır.

**Əsas qaydalar:**

```python
# ✅ DÜZGÜN
def calculate_total_price(items, discount=0):
    """Calculate total price with optional discount."""
    subtotal = sum(item.price * item.quantity for item in items)
    total = subtotal - (subtotal * discount / 100)
    return round(total, 2)

# ❌ YANLIŞ
def CalculateTotalPrice(items,discount=0):
    subtotal=sum(item.price*item.quantity for item in items)
    total=subtotal-(subtotal*discount/100)
    return round(total,2)
```

### **Naming Conventions**

| Element | Convention | Nümunə |
|---------|------------|--------|
| **Variables** | snake_case | `user_email`, `total_price` |
| **Functions** | snake_case | `get_user_orders()`, `send_email()` |
| **Classes** | PascalCase | `BookManager`, `OrderService` |
| **Constants** | UPPER_SNAKE_CASE | `MAX_UPLOAD_SIZE`, `DEFAULT_LANGUAGE` |
| **Private** | _leading_underscore | `_internal_method()` |
| **Modules** | lowercase | `utils.py`, `services.py` |

### **Imports**

```python
# ✅ DÜZGÜN - Sıralama
# 1. Standard library
import os
import sys
from datetime import datetime

# 2. Third-party
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers

# 3. Local
from apps.books.models import Book
from apps.orders.services import OrderService
from .utils import generate_order_number

# ❌ YANLIŞ - Qarışıq
from apps.books.models import Book
import os
from django.db import models
from .utils import generate_order_number
```

### **Docstrings**

Bütün functions, classes və modules docstring-ə malik olmalıdır.

```python
# ✅ DÜZGÜN
def create_order(user, cart_items, shipping_address):
    """
    Create a new order from cart items.
    
    Args:
        user (User): The user placing the order
        cart_items (QuerySet): Cart items to include in order
        shipping_address (dict): Shipping address details
        
    Returns:
        Order: The created order instance
        
    Raises:
        ValidationError: If cart is empty or address is invalid
    """
    if not cart_items.exists():
        raise ValidationError("Cart is empty")
    
    # Implementation...
    return order

# ❌ YANLIŞ - Docstring yoxdur
def create_order(user, cart_items, shipping_address):
    if not cart_items.exists():
        raise ValidationError("Cart is empty")
    return order
```

### **Type Hints (Recommended)**

```python
# ✅ DÜZGÜN
from typing import List, Optional
from decimal import Decimal

def calculate_discount(
    price: Decimal, 
    discount_percentage: int
) -> Decimal:
    """Calculate discounted price."""
    return price - (price * discount_percentage / 100)

def get_user_orders(user_id: int) -> List['Order']:
    """Get all orders for a user."""
    return Order.objects.filter(user_id=user_id)
```

---

## 🎨 Django-Specific Standards

### **Models**

```python
# ✅ DÜZGÜN
class Book(models.Model):
    """Book model representing a book in the catalog."""
    
    # Fields grouped logically
    # Basic info
    title = models.CharField(max_length=500)
    slug = models.SlugField(unique=True)
    isbn = models.CharField(max_length=13, unique=True)
    
    # Relationships
    authors = models.ManyToManyField('Author', related_name='books')
    publisher = models.ForeignKey('Publisher', on_delete=models.SET_NULL, null=True)
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    
    # Timestamps (always at the end)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Kitab'
        verbose_name_plural = 'Kitablar'
        indexes = [
            models.Index(fields=['isbn']),
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('books:detail', kwargs={'slug': self.slug})
    
    @property
    def final_price(self):
        """Return discount price if available, otherwise regular price."""
        return self.discount_price or self.price
    
    def is_in_stock(self):
        """Check if book is in stock."""
        return self.stock > 0
```

**Model Qaydaları:**
- ✅ Docstring əlavə et
- ✅ Fields-i məntiqi qruplara ayır
- ✅ Timestamps sonda olsun
- ✅ `__str__()` method mütləq olsun
- ✅ `get_absolute_url()` əlavə et
- ✅ Properties və methods aydın adlandır

### **Views**

```python
# ✅ DÜZGÜN - Class-Based View
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

class BookListView(ListView):
    """Display list of books with filtering."""
    
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 24
    
    def get_queryset(self):
        """Filter books based on query parameters."""
        queryset = super().get_queryset()
        
        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)
        
        # Filter by price range
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset.select_related('publisher').prefetch_related('authors')
    
    def get_context_data(self, **kwargs):
        """Add extra context."""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        return context

# ✅ DÜZGÜN - Function-Based View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, book_id):
    """Add book to shopping cart."""
    book = get_object_or_404(Book, id=book_id, is_active=True)
    
    if not book.is_in_stock():
        messages.error(request, 'Bu kitab stokda yoxdur.')
        return redirect('books:detail', slug=book.slug)
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book,
        defaults={'price': book.final_price}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{book.title} səbətə əlavə edildi.')
    return redirect('cart:detail')
```

**View Qaydaları:**
- ✅ Class-based views üstünlük təşkil edir (reusability)
- ✅ Function-based views sadə actions üçün
- ✅ Docstrings əlavə et
- ✅ QuerySet optimization (select_related, prefetch_related)
- ✅ Error handling (404, validation)
- ✅ User feedback (messages framework)

### **URLs**

```python
# ✅ DÜZGÜN
from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.BookListView.as_view(), name='list'),
    path('<slug:slug>/', views.BookDetailView.as_view(), name='detail'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category'),
    path('author/<slug:slug>/', views.AuthorView.as_view(), name='author'),
    path('search/', views.BookSearchView.as_view(), name='search'),
]
```

**URL Qaydaları:**
- ✅ `app_name` mütləq təyin et
- ✅ URL names descriptive olsun
- ✅ Slug-based URLs istifadə et (SEO)
- ✅ RESTful naming conventions

### **Forms**

```python
# ✅ DÜZGÜN
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    """Form for submitting book reviews."""
    
    class Meta:
        model = Review
        fields = ['rating', 'title', 'content']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Rəy başlığı'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 5,
                'placeholder': 'Rəyinizi yazın...'
            }),
        }
        labels = {
            'rating': 'Reytinq',
            'title': 'Başlıq',
            'content': 'Rəy',
        }
    
    def clean_content(self):
        """Validate review content."""
        content = self.cleaned_data.get('content')
        if len(content) < 20:
            raise forms.ValidationError('Rəy ən azı 20 simvol olmalıdır.')
        return content
```

**Form Qaydaları:**
- ✅ ModelForm istifadə et (DRY)
- ✅ Widgets və labels təyin et
- ✅ Custom validation əlavə et
- ✅ Tailwind CSS classes istifadə et

### **Templates**

```django
{# ✅ DÜZGÜN #}
{% extends 'base.html' %}
{% load i18n static %}

{% block title %}{{ book.title }} - Olric Bookstore{% endblock %}

{% block content %}
<div class="container mx-auto px-4 py-8">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        {# Book image #}
        <div class="book-image">
            <img 
                src="{{ book.cover_image.url }}" 
                alt="{{ book.title }}"
                class="w-full rounded-lg shadow-lg"
            >
        </div>
        
        {# Book details #}
        <div class="book-details">
            <h1 class="text-3xl font-bold mb-4">{{ book.title }}</h1>
            
            {% if book.authors.exists %}
                <p class="text-gray-600 mb-2">
                    {% trans "Müəllif" %}: 
                    {% for author in book.authors.all %}
                        <a href="{% url 'books:author' author.slug %}" class="text-blue-600 hover:underline">
                            {{ author.name }}
                        </a>{% if not forloop.last %}, {% endif %}
                    {% endfor %}
                </p>
            {% endif %}
            
            {# Price #}
            <div class="price mb-4">
                {% if book.discount_price %}
                    <span class="text-2xl font-bold text-red-600">{{ book.discount_price }} ₼</span>
                    <span class="text-lg line-through text-gray-500 ml-2">{{ book.price }} ₼</span>
                {% else %}
                    <span class="text-2xl font-bold">{{ book.price }} ₼</span>
                {% endif %}
            </div>
            
            {# Add to cart button #}
            {% if book.is_in_stock %}
                <button 
                    id="add-to-cart-btn" 
                    data-book-id="{{ book.id }}"
                    class="btn btn-primary w-full"
                >
                    {% trans "Səbətə əlavə et" %}
                </button>
            {% else %}
                <button class="btn btn-disabled w-full" disabled>
                    {% trans "Stokda yoxdur" %}
                </button>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="{% static 'js/book-detail.js' %}"></script>
{% endblock %}
```

**Template Qaydaları:**
- ✅ Template inheritance istifadə et
- ✅ `{% load %}` tags başda olsun
- ✅ Comments əlavə et (`{# #}`)
- ✅ i18n istifadə et (`{% trans %}`)
- ✅ Tailwind CSS classes
- ✅ Semantic HTML
- ✅ Accessibility (alt texts, ARIA labels)

---

## 💾 Database Standards

### **Migrations**

```bash
# ✅ DÜZGÜN - Descriptive migration names
python manage.py makemigrations books --name add_bestseller_field
python manage.py makemigrations orders --name add_order_status_choices

# ❌ YANLIŞ - Auto-generated names
python manage.py makemigrations
```

**Migration Qaydaları:**
- ✅ Descriptive names istifadə et
- ✅ Hər dəfə migrate et (test environment-də)
- ✅ Rollback plan hazırla
- ✅ Data migrations ayrıca yaz

### **QuerySet Optimization**

```python
# ✅ DÜZGÜN - Optimized
books = Book.objects.select_related('publisher').prefetch_related('authors', 'categories')

# ❌ YANLIŞ - N+1 problem
books = Book.objects.all()
for book in books:
    print(book.publisher.name)  # Extra query hər dəfə!
```

**QuerySet Qaydaları:**
- ✅ `select_related()` ForeignKey üçün
- ✅ `prefetch_related()` ManyToMany üçün
- ✅ `only()` / `defer()` lazım olan fields üçün
- ✅ `count()` əvəzinə `exists()` boolean check üçün
- ✅ Bulk operations (`bulk_create()`, `bulk_update()`)

---

## 🎨 Frontend Standards

### **HTML**

```html
<!-- ✅ DÜZGÜN -->
<article class="book-card" itemscope itemtype="http://schema.org/Book">
    <img 
        src="{{ book.cover_image.url }}" 
        alt="{{ book.title }}"
        class="book-cover"
        loading="lazy"
    >
    <h3 class="book-title" itemprop="name">{{ book.title }}</h3>
    <p class="book-author" itemprop="author">{{ book.authors.first.name }}</p>
    <span class="book-price" itemprop="price">{{ book.price }} ₼</span>
</article>

<!-- ❌ YANLIŞ -->
<div class="book">
    <img src="{{ book.cover_image.url }}">
    <div>{{ book.title }}</div>
    <div>{{ book.authors.first.name }}</div>
    <div>{{ book.price }} ₼</div>
</div>
```

**HTML Qaydaları:**
- ✅ Semantic HTML5 tags
- ✅ Schema.org markup (SEO)
- ✅ Alt texts hər şəkil üçün
- ✅ Lazy loading images
- ✅ Unique IDs

### **CSS (Tailwind)**

```html
<!-- ✅ DÜZGÜN - Utility classes -->
<button class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition duration-200">
    Səbətə əlavə et
</button>

<!-- ✅ DÜZGÜN - Custom component class (input.css) -->
<button class="btn btn-primary">
    Səbətə əlavə et
</button>
```

```css
/* input.css */
@layer components {
    .btn {
        @apply font-bold py-2 px-4 rounded transition duration-200;
    }
    
    .btn-primary {
        @apply bg-blue-600 hover:bg-blue-700 text-white;
    }
    
    .btn-secondary {
        @apply bg-gray-600 hover:bg-gray-700 text-white;
    }
}
```

**CSS Qaydaları:**
- ✅ Tailwind utility classes istifadə et
- ✅ Təkrarlanan patterns üçün component classes yarat
- ✅ Responsive design (`md:`, `lg:` prefixes)
- ✅ Dark mode support (gələcək)

### **JavaScript (jQuery)**

```javascript
// ✅ DÜZGÜN
// static/js/cart.js
(function($) {
    'use strict';
    
    const Cart = {
        /**
         * Initialize cart functionality
         */
        init: function() {
            this.bindEvents();
        },
        
        /**
         * Bind event listeners
         */
        bindEvents: function() {
            $(document).on('click', '.add-to-cart-btn', this.addToCart);
            $(document).on('click', '.remove-from-cart-btn', this.removeFromCart);
            $(document).on('change', '.cart-quantity-input', this.updateQuantity);
        },
        
        /**
         * Add item to cart
         */
        addToCart: function(e) {
            e.preventDefault();
            
            const $btn = $(this);
            const bookId = $btn.data('book-id');
            
            $.ajax({
                url: '/cart/add/',
                method: 'POST',
                data: {
                    book_id: bookId,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(response) {
                    Cart.showMessage('success', response.message);
                    Cart.updateCartCount(response.cart_count);
                },
                error: function(xhr) {
                    Cart.showMessage('error', xhr.responseJSON.error);
                }
            });
        },
        
        /**
         * Show notification message
         */
        showMessage: function(type, message) {
            // Implementation...
        },
        
        /**
         * Update cart count in header
         */
        updateCartCount: function(count) {
            $('.cart-count').text(count);
        }
    };
    
    // Initialize on document ready
    $(document).ready(function() {
        Cart.init();
    });
    
})(jQuery);
```

**JavaScript Qaydaları:**
- ✅ IIFE pattern istifadə et
- ✅ 'use strict' mode
- ✅ Object-based organization
- ✅ JSDoc comments
- ✅ Error handling
- ✅ CSRF token hər AJAX request-də
- ✅ Separate files (cart.js, wishlist.js, etc.)

---

## 🔒 Security Standards

### **1. Input Validation**

```python
# ✅ DÜZGÜN
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    content = models.TextField(validators=[MinLengthValidator(20)])
```

### **2. XSS Protection**

```django
{# ✅ DÜZGÜN - Auto-escaped #}
<p>{{ user_input }}</p>

{# ⚠️ DİQQƏTLƏ - Manual escape disable #}
<p>{{ user_input|safe }}</p>  {# Only if you trust the source! #}
```

### **3. CSRF Protection**

```django
{# ✅ DÜZGÜN #}
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Göndər</button>
</form>
```

```javascript
// ✅ DÜZGÜN - AJAX
$.ajax({
    url: '/api/endpoint/',
    method: 'POST',
    data: {
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        // other data...
    }
});
```

### **4. SQL Injection Protection**

```python
# ✅ DÜZGÜN - ORM
books = Book.objects.filter(title__icontains=search_query)

# ❌ YANLIŞ - Raw SQL (avoid!)
cursor.execute(f"SELECT * FROM books WHERE title LIKE '%{search_query}%'")
```

---

## 🧪 Testing Standards

### **Unit Tests**

```python
# tests/test_models.py
from django.test import TestCase
from apps.books.models import Book, Author

class BookModelTest(TestCase):
    """Test Book model."""
    
    def setUp(self):
        """Set up test data."""
        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(
            title='Test Book',
            isbn='1234567890123',
            price=29.99
        )
        self.book.authors.add(self.author)
    
    def test_book_str(self):
        """Test __str__ method."""
        self.assertEqual(str(self.book), 'Test Book')
    
    def test_final_price_without_discount(self):
        """Test final_price property without discount."""
        self.assertEqual(self.book.final_price, 29.99)
    
    def test_final_price_with_discount(self):
        """Test final_price property with discount."""
        self.book.discount_price = 24.99
        self.book.save()
        self.assertEqual(self.book.final_price, 24.99)
    
    def test_is_in_stock(self):
        """Test is_in_stock method."""
        self.book.stock = 0
        self.assertFalse(self.book.is_in_stock())
        
        self.book.stock = 5
        self.assertTrue(self.book.is_in_stock())
```

**Testing Qaydaları:**
- ✅ Hər app üçün tests/ folder
- ✅ Descriptive test names
- ✅ setUp() method istifadə et
- ✅ Docstrings əlavə et
- ✅ Minimum 80% coverage

---

## 📝 Git Standards

### **Commit Messages**

```bash
# ✅ DÜZGÜN
git commit -m "feat: Add wishlist functionality"
git commit -m "fix: Fix cart quantity update bug"
git commit -m "docs: Update README with deployment instructions"
git commit -m "refactor: Optimize book queryset in list view"
git commit -m "test: Add tests for order creation"

# ❌ YANLIŞ
git commit -m "update"
git commit -m "fix bug"
git commit -m "changes"
```

**Commit Prefixes:**
- `feat:` - Yeni feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Code formatting
- `refactor:` - Code refactoring
- `test:` - Tests
- `chore:` - Build, dependencies

### **Branch Naming**

```bash
# ✅ DÜZGÜN
feature/wishlist
feature/payment-integration
fix/cart-quantity-bug
hotfix/security-patch
refactor/optimize-queries

# ❌ YANLIŞ
new-feature
fix
update
```

---

## 📚 Documentation Standards

### **Code Comments**

```python
# ✅ DÜZGÜN - Necessary comments
def calculate_shipping_cost(city, weight):
    """
    Calculate shipping cost based on city and package weight.
    
    Shipping rates:
    - Baku: 3 AZN (base) + 0.5 AZN per kg
    - Other cities: 5 AZN (base) + 1 AZN per kg
    """
    if city.lower() == 'baku':
        base_cost = 3
        per_kg_cost = 0.5
    else:
        base_cost = 5
        per_kg_cost = 1
    
    # Convert grams to kg
    weight_kg = weight / 1000
    
    return base_cost + (weight_kg * per_kg_cost)

# ❌ YANLIŞ - Obvious comments
# Increment i by 1
i += 1

# Get all books
books = Book.objects.all()
```

**Comment Qaydaları:**
- ✅ WHY, not WHAT
- ✅ Complex logic izah et
- ✅ TODO/FIXME markers istifadə et
- ❌ Obvious statements comment etmə

---

## 🎯 Code Review Checklist

### **Before Submitting PR:**
- [ ] PEP 8 compliance
- [ ] Docstrings əlavə edilib
- [ ] Tests yazılıb və pass edir
- [ ] Migrations yaradılıb (lazım olarsa)
- [ ] README/docs yenilənib (lazım olarsa)
- [ ] No console.log() / print() statements
- [ ] No commented-out code
- [ ] CSRF tokens əlavə edilib (forms/AJAX)
- [ ] QuerySet optimization
- [ ] Error handling

### **Reviewer Checklist:**
- [ ] Code readable və maintainable-dır
- [ ] Logic düzgündür
- [ ] Security issues yoxdur
- [ ] Performance issues yoxdur
- [ ] Tests adequate-dir
- [ ] Documentation kifayətdir

---

## 🚀 Xülasə

Bu qaydalar Olric Bookstore layihəsinin **code quality**, **maintainability** və **scalability**-ni təmin etmək üçün hazırlanıb.

**Əsas prinsiplər:**
- ✅ Clean Code
- ✅ DRY, KISS, YAGNI
- ✅ PEP 8 Compliance
- ✅ Security First
- ✅ Test Coverage
- ✅ Documentation

---

**Sənəd versiyası:** 1.0  
**Son yenilənmə:** 2026-01-21  
**Müəllif:** Olric Bookstore Development Team
