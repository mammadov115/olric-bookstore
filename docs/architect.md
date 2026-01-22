# 🏗️ System Architecture - Olric Bookstore

## 📋 Ümumi Baxış

Bu sənəd Olric Bookstore layihəsinin sistem arxitekturasını, Django apps strukturunu, database schema-nı və komponent qarşılıqlı əlaqələrini ətraflı şəkildə izah edir.

---

## 🎯 Arxitektur Prinsipləri

### **1. Monolith Architecture**
- ✅ Bütün funksionallıq bir Django project-də
- ✅ Shared database (MySQL)
- ✅ Modular apps (separation of concerns)
- ✅ Gələcəkdə microservices-ə keçid mümkündür

### **2. MVT Pattern (Model-View-Template)**
- **Model:** Database layer (Django ORM)
- **View:** Business logic layer
- **Template:** Presentation layer (HTML + Tailwind)

### **3. Separation of Concerns**
- Hər bir Django app öz məsuliyyətinə cavabdehdir
- Reusable components
- Minimal dependencies between apps

---

## 📁 Project Structure

```
olric-bookstore/
├── config/                      # Project configuration
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py             # Base settings
│   │   ├── development.py      # Development settings
│   │   ├── production.py       # Production settings
│   │   └── testing.py          # Testing settings
│   ├── urls.py                 # Main URL configuration
│   ├── wsgi.py                 # WSGI configuration
│   └── asgi.py                 # ASGI configuration (future)
│
├── apps/                        # Django applications
│   ├── accounts/               # User management
│   ├── books/                  # Book catalog
│   ├── cart/                   # Shopping cart
│   ├── orders/                 # Order management
│   ├── payments/               # Payment processing
│   ├── delivery/               # Delivery tracking
│   ├── reviews/                # Book reviews & ratings
│   ├── wishlist/               # User wishlist
│   ├── coupons/                # Discount coupons
│   ├── notifications/          # Email & SMS notifications
│   └── dashboard/              # Custom admin panel
│
├── templates/                   # HTML templates
│   ├── base.html               # Base template
│   ├── includes/               # Reusable components
│   │   ├── header.html
│   │   ├── footer.html
│   │   ├── navbar.html
│   │   └── sidebar.html
│   ├── accounts/               # Account templates
│   ├── books/                  # Book templates
│   ├── cart/                   # Cart templates
│   ├── orders/                 # Order templates
│   ├── dashboard/              # Admin panel templates
│   └── errors/                 # Error pages (404, 500)
│
├── static/                      # Static files
│   ├── css/
│   │   ├── input.css           # Tailwind input
│   │   └── output.css          # Tailwind compiled
│   ├── js/
│   │   ├── main.js
│   │   ├── cart.js
│   │   ├── wishlist.js
│   │   ├── search.js
│   │   └── checkout.js
│   ├── images/
│   │   ├── logo.png
│   │   ├── placeholder.jpg
│   │   └── banners/
│   └── fonts/
│
├── media/                       # User uploaded files
│   ├── books/                  # Book covers
│   │   └── covers/
│   ├── profiles/               # User avatars
│   └── temp/                   # Temporary files
│
├── locale/                      # Translations
│   ├── az/                     # Azerbaijani
│   └── en/                     # English
│
├── tests/                       # Test files
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
├── scripts/                     # Utility scripts
│   ├── seed_data.py            # Fake data generation
│   ├── import_books.py         # Google Books API import
│   └── backup_db.py            # Database backup
│
├── docs/                        # Documentation
│   ├── tech-stack.md
│   ├── architect.md
│   ├── rules.md
│   ├── database-schema.md
│   ├── api-endpoints.md
│   ├── deployment-guide.md
│   ├── security-checklist.md
│   └── testing-guide.md
│
├── .env                         # Environment variables
├── .env.example                # Environment template
├── .gitignore
├── requirements.txt            # Python dependencies
├── requirements-dev.txt        # Development dependencies
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── tailwind.config.js
├── package.json                # Node dependencies (Tailwind)
└── README.md
```

---

## 🗂️ Django Apps - Detallı Təsvir

### **1. accounts/** - User Management

**Məsuliyyət:** İstifadəçi idarəetmə, authentication, authorization

**Models:**
```python
# models.py
class User(AbstractUser):
    """Custom User model"""
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='profiles/', blank=True)
    
    # Role management
    ROLE_CHOICES = [
        ('customer', 'Müştəri'),
        ('courier', 'Kuryer'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    
    # Preferences
    preferred_language = models.CharField(max_length=5, default='az')
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserProfile(models.Model):
    """Extended user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    favorite_genres = models.JSONField(default=list)
    reading_preferences = models.JSONField(default=dict)
```

**Views:**
- Registration, Login, Logout
- Profile management
- Password reset
- Role-based dashboards

**URLs:**
- `/accounts/register/`
- `/accounts/login/`
- `/accounts/logout/`
- `/accounts/profile/`
- `/accounts/profile/edit/`

---

### **2. books/** - Book Catalog

**Məsuliyyət:** Kitab kataloqu, axtarış, filtrasiya

**Models:**
```python
# models.py
class Category(models.Model):
    """Book categories/genres"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='categories/', blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

class Author(models.Model):
    """Book authors"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='authors/', blank=True)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)

class Publisher(models.Model):
    """Book publishers"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='publishers/', blank=True)

class Book(models.Model):
    """Main book model"""
    # Basic info
    title = models.CharField(max_length=500)
    slug = models.SlugField(unique=True)
    subtitle = models.CharField(max_length=500, blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    isbn10 = models.CharField(max_length=10, blank=True)
    
    # Relationships
    authors = models.ManyToManyField(Author, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True)
    categories = models.ManyToManyField(Category, related_name='books')
    
    # Content
    description = models.TextField()
    table_of_contents = models.TextField(blank=True)
    
    # Publication
    publication_date = models.DateField(null=True, blank=True)
    edition = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=10, default='az')
    
    # Physical properties
    pages = models.IntegerField(null=True, blank=True)
    FORMAT_CHOICES = [
        ('hardcover', 'Hardcover'),
        ('paperback', 'Paperback'),
        ('ebook', 'E-book'),
    ]
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES)
    dimensions = models.CharField(max_length=100, blank=True)  # "20x15x2 cm"
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # grams
    
    # Images
    cover_image = models.ImageField(upload_to='books/covers/')
    back_cover_image = models.ImageField(upload_to='books/covers/', blank=True)
    
    # Pricing & Stock
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(default=0)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)
    
    # Stats
    views_count = models.IntegerField(default=0)
    sales_count = models.IntegerField(default=0)
    
    # External API
    google_books_id = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['isbn']),
            models.Index(fields=['slug']),
            models.Index(fields=['-created_at']),
        ]

class BookImage(models.Model):
    """Additional book images"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='books/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
```

**Views:**
- Book list (with filters)
- Book detail
- Search functionality
- Category pages
- Author pages
- Publisher pages

**URLs:**
- `/books/`
- `/books/<slug>/`
- `/books/category/<slug>/`
- `/books/author/<slug>/`
- `/books/search/`

---

### **3. cart/** - Shopping Cart

**Məsuliyyət:** Səbət idarəetmə

**Models:**
```python
# models.py
class Cart(models.Model):
    """Shopping cart"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True)  # For anonymous users
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    """Cart items"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of adding
    added_at = models.DateTimeField(auto_now_add=True)
```

**Views:**
- Add to cart (AJAX)
- Update quantity (AJAX)
- Remove from cart (AJAX)
- Cart page
- Cart summary

**URLs:**
- `/cart/`
- `/cart/add/`
- `/cart/update/`
- `/cart/remove/`

---

### **4. orders/** - Order Management

**Məsuliyyət:** Sifariş idarəetmə

**Models:**
```python
# models.py
class Order(models.Model):
    """Customer orders"""
    # Order info
    order_number = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    # Billing info
    billing_name = models.CharField(max_length=200)
    billing_email = models.EmailField()
    billing_phone = models.CharField(max_length=20)
    billing_address = models.TextField()
    billing_city = models.CharField(max_length=100)
    billing_postal_code = models.CharField(max_length=10)
    
    # Shipping info (can be different from billing)
    shipping_name = models.CharField(max_length=200)
    shipping_phone = models.CharField(max_length=20)
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_postal_code = models.CharField(max_length=10)
    
    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Coupon
    coupon = models.ForeignKey('coupons.Coupon', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Payment
    PAYMENT_METHOD_CHOICES = [
        ('online', 'Online Ödəniş'),
        ('cash', 'Nağd Ödəniş'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    
    STATUS_CHOICES = [
        ('pending', 'Gözləyir'),
        ('confirmed', 'Təsdiqləndi'),
        ('processing', 'Hazırlanır'),
        ('shipped', 'Göndərildi'),
        ('delivered', 'Çatdırıldı'),
        ('cancelled', 'Ləğv edildi'),
        ('refunded', 'Geri qaytarıldı'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Notes
    customer_notes = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']

class OrderItem(models.Model):
    """Order line items"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey('books.Book', on_delete=models.SET_NULL, null=True)
    book_title = models.CharField(max_length=500)  # Snapshot
    book_isbn = models.CharField(max_length=13)    # Snapshot
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
```

**Views:**
- Checkout process
- Order confirmation
- Order history
- Order detail
- Order tracking

**URLs:**
- `/orders/checkout/`
- `/orders/confirmation/<order_number>/`
- `/orders/history/`
- `/orders/<order_number>/`

---

### **5. payments/** - Payment Processing

**Məsuliyyət:** Ödəniş prosesi (MilliÖn integration)

**Models:**
```python
# models.py
class Payment(models.Model):
    """Payment transactions"""
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='payments')
    
    # MilliÖn info
    transaction_id = models.CharField(max_length=100, unique=True)
    millipay_order_id = models.CharField(max_length=100, blank=True)
    
    # Amount
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='AZN')
    
    # Status
    STATUS_CHOICES = [
        ('pending', 'Gözləyir'),
        ('processing', 'İşlənir'),
        ('completed', 'Tamamlandı'),
        ('failed', 'Uğursuz'),
        ('refunded', 'Geri qaytarıldı'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Card info (masked)
    card_mask = models.CharField(max_length=20, blank=True)  # "****1234"
    card_type = models.CharField(max_length=20, blank=True)  # "Visa", "Mastercard"
    
    # Response data
    response_data = models.JSONField(default=dict)
    error_message = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
```

**Services:**
```python
# services.py
class MilliPayService:
    def create_payment(self, order):
        """Create payment request"""
        pass
    
    def verify_payment(self, transaction_id):
        """Verify payment status"""
        pass
    
    def process_callback(self, data):
        """Process MilliÖn callback"""
        pass
    
    def refund_payment(self, payment):
        """Refund payment"""
        pass
```

**URLs:**
- `/payments/initiate/<order_number>/`
- `/payments/callback/`
- `/payments/success/<order_number>/`
- `/payments/failed/<order_number>/`

---

### **6. delivery/** - Delivery Tracking

**Məsuliyyət:** Çatdırılma tracking

**Models:**
```python
# models.py
class Courier(models.Model):
    """Courier/Driver"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=50)
    vehicle_number = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    current_location_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_location_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    last_location_update = models.DateTimeField(null=True, blank=True)

class Delivery(models.Model):
    """Delivery tracking"""
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='delivery')
    courier = models.ForeignKey(Courier, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Tracking
    tracking_number = models.CharField(max_length=50, unique=True)
    
    STATUS_CHOICES = [
        ('pending', 'Gözləyir'),
        ('assigned', 'Kuryerə təyin edildi'),
        ('picked_up', 'Götürüldü'),
        ('in_transit', 'Yoldadır'),
        ('delivered', 'Çatdırıldı'),
        ('failed', 'Çatdırılmadı'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Estimated delivery
    estimated_delivery_date = models.DateField(null=True, blank=True)
    estimated_delivery_time = models.TimeField(null=True, blank=True)
    
    # Actual delivery
    delivered_at = models.DateTimeField(null=True, blank=True)
    delivered_to = models.CharField(max_length=200, blank=True)
    signature = models.ImageField(upload_to='delivery/signatures/', blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class DeliveryStatusUpdate(models.Model):
    """Delivery status history"""
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='status_updates')
    status = models.CharField(max_length=20)
    location = models.CharField(max_length=200, blank=True)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
```

**URLs:**
- `/delivery/track/<tracking_number>/`
- `/delivery/update-location/` (AJAX - courier app)

---

### **7. reviews/** - Reviews & Ratings

**Məsuliyyət:** Kitab rəyləri və reytinqlər

**Models:**
```python
# models.py
class Review(models.Model):
    """Book reviews"""
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Rating (1-5 stars)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    
    # Review
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    # Moderation
    is_approved = models.BooleanField(default=False)
    is_verified_purchase = models.BooleanField(default=False)
    
    # Helpfulness
    helpful_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['book', 'user']
        ordering = ['-created_at']

class ReviewHelpful(models.Model):
    """Track who found review helpful"""
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['review', 'user']
```

**URLs:**
- `/reviews/add/<book_slug>/`
- `/reviews/<review_id>/helpful/` (AJAX)

---

### **8. wishlist/** - User Wishlist

**Məsuliyyət:** İstək siyahısı

**Models:**
```python
# models.py
class Wishlist(models.Model):
    """User wishlist"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'book']
        ordering = ['-added_at']
```

**URLs:**
- `/wishlist/`
- `/wishlist/add/` (AJAX)
- `/wishlist/remove/` (AJAX)

---

### **9. coupons/** - Discount Coupons

**Məsuliyyət:** Endirim kuponları

**Models:**
```python
# models.py
class Coupon(models.Model):
    """Discount coupons"""
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    # Discount
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Faiz'),
        ('fixed', 'Sabit məbləğ'),
    ]
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Conditions
    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Usage limits
    usage_limit = models.IntegerField(null=True, blank=True)  # Total uses
    usage_limit_per_user = models.IntegerField(default=1)
    usage_count = models.IntegerField(default=0)
    
    # Validity
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    
    # Status
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

class CouponUsage(models.Model):
    """Track coupon usage"""
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    used_at = models.DateTimeField(auto_now_add=True)
```

**URLs:**
- `/coupons/validate/` (AJAX)

---

### **10. notifications/** - Notifications

**Məsuliyyət:** Email və SMS bildirişləri

**Models:**
```python
# models.py
class EmailNotification(models.Model):
    """Email notification log"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    to_email = models.EmailField()
    subject = models.CharField(max_length=200)
    template = models.CharField(max_length=100)
    context_data = models.JSONField(default=dict)
    
    STATUS_CHOICES = [
        ('pending', 'Gözləyir'),
        ('sent', 'Göndərildi'),
        ('failed', 'Uğursuz'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class SMSNotification(models.Model):
    """SMS notification log"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    to_phone = models.CharField(max_length=20)
    message = models.TextField()
    
    STATUS_CHOICES = [
        ('pending', 'Gözləyir'),
        ('sent', 'Göndərildi'),
        ('failed', 'Uğursuz'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

**Services:**
```python
# services.py
class NotificationService:
    def send_order_confirmation(self, order):
        """Send order confirmation email & SMS"""
        pass
    
    def send_shipping_update(self, delivery):
        """Send shipping update"""
        pass
    
    def send_delivery_notification(self, delivery):
        """Send delivery notification"""
        pass
```

---

### **11. dashboard/** - Custom Admin Panel

**Məsuliyyət:** Custom admin panel (Django templates + Tailwind)

**Views:**
- Dashboard overview (stats, charts)
- Book management (CRUD)
- Order management
- Customer management
- Courier management
- Coupon management
- Review moderation
- Reports & analytics

**URLs:**
- `/dashboard/`
- `/dashboard/books/`
- `/dashboard/orders/`
- `/dashboard/customers/`
- `/dashboard/couriers/`
- `/dashboard/coupons/`
- `/dashboard/reviews/`
- `/dashboard/reports/`

---

## 🗄️ Database Schema Overview

```
┌─────────────┐
│    User     │
└──────┬──────┘
       │
       ├──────────┬──────────┬──────────┬──────────┐
       │          │          │          │          │
┌──────▼──────┐ ┌▼────────┐ ┌▼────────┐ ┌▼────────┐ ┌▼────────┐
│ UserProfile │ │  Order  │ │Wishlist │ │ Review  │ │  Cart   │
└─────────────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘
                     │           │           │           │
              ┌──────▼──────┐    │           │    ┌──────▼──────┐
              │  OrderItem  │    │           │    │  CartItem   │
              └──────┬──────┘    │           │    └──────┬──────┘
                     │           │           │           │
                ┌────▼───────────▼───────────▼───────────▼────┐
                │                 Book                         │
                └────┬──────────┬──────────┬──────────┬────────┘
                     │          │          │          │
              ┌──────▼──────┐ ┌▼────────┐ ┌▼────────┐ ┌▼────────┐
              │   Author    │ │Publisher│ │Category │ │BookImage│
              └─────────────┘ └─────────┘ └─────────┘ └─────────┘

┌─────────────┐
│    Order    │
└──────┬──────┘
       │
       ├──────────┬──────────┐
       │          │          │
┌──────▼──────┐ ┌▼────────┐ ┌▼────────┐
│   Payment   │ │Delivery │ │ Coupon  │
└─────────────┘ └────┬────┘ └─────────┘
                     │
              ┌──────▼──────────────┐
              │ DeliveryStatusUpdate│
              └─────────────────────┘
```

---

## 🔄 Request Flow

### **1. Book Browsing:**
```
User → URL → View → QuerySet → Template → Response
```

### **2. Add to Cart (AJAX):**
```
User → AJAX Request → View → Cart Model → JSON Response → Update UI
```

### **3. Checkout Process:**
```
User → Cart → Checkout Form → Create Order → Payment Gateway → Callback → Update Order → Confirmation
```

### **4. Payment Flow:**
```
Order Created → MilliÖn Payment Request → Redirect to MilliÖn → User Pays → 
Callback → Verify Payment → Update Order Status → Send Notifications
```

---

## 🎯 Xülasə

Olric Bookstore layihəsi **modular monolith** arxitekturası ilə qurulub. Hər bir Django app öz məsuliyyətinə cavabdehdir və minimal dependencies ilə işləyir. Bu struktur:

✅ **Maintainable** - Asan dəyişikliklər  
✅ **Scalable** - Gələcəkdə microservices-ə keçid mümkün  
✅ **Testable** - Hər app ayrıca test edilə bilər  
✅ **Reusable** - Komponentlər yenidən istifadə oluna bilər  

---

**Sənəd versiyası:** 1.0  
**Son yenilənmə:** 2026-01-21  
**Müəllif:** Olric Bookstore Development Team
