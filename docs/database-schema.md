# 🗄️ Database Schema - Olric Bookstore

## 📋 Ümumi Baxış

Bu sənəd Olric Bookstore layihəsinin verilənlər bazası strukturunu, table relationships, indexes və constraints-ləri ətraflı şəkildə izah edir.

---

## 🎯 Database Information

- **Database Type:** MySQL 8.x (Initial), PostgreSQL (Future)
- **ORM:** Django ORM
- **Character Set:** utf8mb4
- **Collation:** utf8mb4_unicode_ci
- **Engine:** InnoDB

---

## 📊 Entity Relationship Diagram (ERD)

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER MANAGEMENT                          │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐
│     User     │ (Django AbstractUser + Custom Fields)
├──────────────┤
│ id (PK)      │
│ username     │
│ email        │
│ password     │
│ first_name   │
│ last_name    │
│ phone        │
│ address      │
│ city         │
│ postal_code  │
│ role         │ (customer, courier, admin)
│ avatar       │
│ created_at   │
│ updated_at   │
└──────┬───────┘
       │
       │ 1:1
       ▼
┌──────────────┐
│ UserProfile  │
├──────────────┤
│ id (PK)      │
│ user_id (FK) │
│ bio          │
│ preferences  │ (JSON)
└──────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         BOOK CATALOG                             │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐         ┌──────────────┐
│   Category   │         │   Publisher  │
├──────────────┤         ├──────────────┤
│ id (PK)      │         │ id (PK)      │
│ name         │         │ name         │
│ slug (UQ)    │         │ slug (UQ)    │
│ description  │         │ website      │
│ parent_id    │         │ logo         │
│ image        │         └──────┬───────┘
│ is_active    │                │
│ order        │                │ 1:N
└──────┬───────┘                │
       │                        │
       │ M:N                    │
       │                        │
       ▼                        ▼
┌──────────────────────────────────────┐
│              Book                     │
├──────────────────────────────────────┤
│ id (PK)                              │
│ title                                │
│ slug (UQ)                            │
│ isbn (UQ)                            │
│ isbn10                               │
│ subtitle                             │
│ description                          │
│ publication_date                     │
│ language                             │
│ pages                                │
│ format                               │
│ cover_image                          │
│ price                                │
│ discount_price                       │
│ stock                                │
│ is_active                            │
│ is_featured                          │
│ is_bestseller                        │
│ views_count                          │
│ sales_count                          │
│ publisher_id (FK)                    │
│ created_at                           │
│ updated_at                           │
└──────┬───────────────────────────────┘
       │
       │ M:N
       ▼
┌──────────────┐
│    Author    │
├──────────────┤
│ id (PK)      │
│ name         │
│ slug (UQ)    │
│ bio          │
│ photo        │
│ birth_date   │
│ nationality  │
└──────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      SHOPPING & ORDERS                           │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐
│     Cart     │
├──────────────┤
│ id (PK)      │
│ user_id (FK) │
│ session_key  │
│ created_at   │
│ updated_at   │
└──────┬───────┘
       │
       │ 1:N
       ▼
┌──────────────┐
│  CartItem    │
├──────────────┤
│ id (PK)      │
│ cart_id (FK) │
│ book_id (FK) │
│ quantity     │
│ price        │
│ added_at     │
└──────────────┘

┌──────────────────────────────────────┐
│              Order                    │
├──────────────────────────────────────┤
│ id (PK)                              │
│ order_number (UQ)                    │
│ user_id (FK)                         │
│ billing_name                         │
│ billing_email                        │
│ billing_phone                        │
│ billing_address                      │
│ shipping_name                        │
│ shipping_address                     │
│ subtotal                             │
│ discount                             │
│ shipping_cost                        │
│ total                                │
│ payment_method                       │
│ status                               │
│ coupon_id (FK)                       │
│ created_at                           │
│ confirmed_at                         │
│ shipped_at                           │
│ delivered_at                         │
└──────┬───────────────────────────────┘
       │
       │ 1:N
       ▼
┌──────────────┐
│  OrderItem   │
├──────────────┤
│ id (PK)      │
│ order_id(FK) │
│ book_id (FK) │
│ book_title   │
│ book_isbn    │
│ quantity     │
│ price        │
│ subtotal     │
└──────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      PAYMENT & DELIVERY                          │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────┐
│             Payment                   │
├──────────────────────────────────────┤
│ id (PK)                              │
│ order_id (FK)                        │
│ transaction_id (UQ)                  │
│ millipay_order_id                    │
│ amount                               │
│ currency                             │
│ status                               │
│ card_mask                            │
│ card_type                            │
│ response_data (JSON)                 │
│ error_message                        │
│ created_at                           │
│ completed_at                         │
└──────────────────────────────────────┘

┌──────────────┐
│   Courier    │
├──────────────┤
│ id (PK)      │
│ user_id (FK) │
│ phone        │
│ vehicle_type │
│ vehicle_no   │
│ is_active    │
│ location_lat │
│ location_lng │
│ updated_at   │
└──────┬───────┘
       │
       │ 1:N
       ▼
┌──────────────────────────────────────┐
│            Delivery                   │
├──────────────────────────────────────┤
│ id (PK)                              │
│ order_id (FK) (1:1)                  │
│ courier_id (FK)                      │
│ tracking_number (UQ)                 │
│ status                               │
│ estimated_delivery_date              │
│ delivered_at                         │
│ delivered_to                         │
│ signature                            │
│ notes                                │
│ created_at                           │
│ updated_at                           │
└──────┬───────────────────────────────┘
       │
       │ 1:N
       ▼
┌──────────────────────────┐
│ DeliveryStatusUpdate     │
├──────────────────────────┤
│ id (PK)                  │
│ delivery_id (FK)         │
│ status                   │
│ location                 │
│ location_lat             │
│ location_lng             │
│ notes                    │
│ created_at               │
└──────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    REVIEWS & WISHLIST                            │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────┐
│             Review                    │
├──────────────────────────────────────┤
│ id (PK)                              │
│ book_id (FK)                         │
│ user_id (FK)                         │
│ rating                               │
│ title                                │
│ content                              │
│ is_approved                          │
│ is_verified_purchase                 │
│ helpful_count                        │
│ created_at                           │
│ updated_at                           │
└──────┬───────────────────────────────┘
       │
       │ 1:N
       ▼
┌──────────────────────────┐
│    ReviewHelpful         │
├──────────────────────────┤
│ id (PK)                  │
│ review_id (FK)           │
│ user_id (FK)             │
│ created_at               │
└──────────────────────────┘

┌──────────────┐
│  Wishlist    │
├──────────────┤
│ id (PK)      │
│ user_id (FK) │
│ book_id (FK) │
│ added_at     │
└──────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         COUPONS                                  │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────┐
│             Coupon                    │
├──────────────────────────────────────┤
│ id (PK)                              │
│ code (UQ)                            │
│ description                          │
│ discount_type                        │
│ discount_value                       │
│ min_purchase_amount                  │
│ max_discount_amount                  │
│ usage_limit                          │
│ usage_limit_per_user                 │
│ usage_count                          │
│ valid_from                           │
│ valid_until                          │
│ is_active                            │
│ created_at                           │
└──────┬───────────────────────────────┘
       │
       │ 1:N
       ▼
┌──────────────────────────┐
│    CouponUsage           │
├──────────────────────────┤
│ id (PK)                  │
│ coupon_id (FK)           │
│ user_id (FK)             │
│ order_id (FK)            │
│ discount_amount          │
│ used_at                  │
└──────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      NOTIFICATIONS                               │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────┐
│       EmailNotification               │
├──────────────────────────────────────┤
│ id (PK)                              │
│ user_id (FK)                         │
│ to_email                             │
│ subject                              │
│ template                             │
│ context_data (JSON)                  │
│ status                               │
│ error_message                        │
│ sent_at                              │
│ created_at                           │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│        SMSNotification                │
├──────────────────────────────────────┤
│ id (PK)                              │
│ user_id (FK)                         │
│ to_phone                             │
│ message                              │
│ status                               │
│ error_message                        │
│ sent_at                              │
│ created_at                           │
└──────────────────────────────────────┘
```

---

## 📋 Table Definitions

### **1. accounts_user**

```sql
CREATE TABLE accounts_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    postal_code VARCHAR(10),
    date_of_birth DATE,
    avatar VARCHAR(100),
    role VARCHAR(20) DEFAULT 'customer',
    preferred_language VARCHAR(5) DEFAULT 'az',
    email_notifications BOOLEAN DEFAULT TRUE,
    sms_notifications BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    is_superuser BOOLEAN DEFAULT FALSE,
    date_joined DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Constraints:**
- `username` UNIQUE
- `email` UNIQUE
- `role` CHECK IN ('customer', 'courier', 'admin')

---

### **2. books_book**

```sql
CREATE TABLE books_book (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    slug VARCHAR(500) UNIQUE NOT NULL,
    subtitle VARCHAR(500),
    isbn VARCHAR(13) UNIQUE NOT NULL,
    isbn10 VARCHAR(10),
    description TEXT NOT NULL,
    table_of_contents TEXT,
    publication_date DATE,
    edition VARCHAR(100),
    language VARCHAR(10) DEFAULT 'az',
    pages INT,
    format VARCHAR(20),
    dimensions VARCHAR(100),
    weight DECIMAL(6,2),
    cover_image VARCHAR(100) NOT NULL,
    back_cover_image VARCHAR(100),
    price DECIMAL(10,2) NOT NULL,
    discount_price DECIMAL(10,2),
    stock INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    is_featured BOOLEAN DEFAULT FALSE,
    is_bestseller BOOLEAN DEFAULT FALSE,
    is_new_arrival BOOLEAN DEFAULT FALSE,
    meta_title VARCHAR(200),
    meta_description TEXT,
    meta_keywords VARCHAR(500),
    views_count INT DEFAULT 0,
    sales_count INT DEFAULT 0,
    google_books_id VARCHAR(100),
    publisher_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (publisher_id) REFERENCES books_publisher(id) ON DELETE SET NULL,
    
    INDEX idx_isbn (isbn),
    INDEX idx_slug (slug),
    INDEX idx_created_at (created_at DESC),
    INDEX idx_price (price),
    INDEX idx_is_active (is_active),
    INDEX idx_is_featured (is_featured),
    FULLTEXT idx_search (title, description)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Constraints:**
- `isbn` UNIQUE
- `slug` UNIQUE
- `price` >= 0
- `stock` >= 0
- `format` CHECK IN ('hardcover', 'paperback', 'ebook')

---

### **3. books_author**

```sql
CREATE TABLE books_author (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(200) UNIQUE NOT NULL,
    bio TEXT,
    photo VARCHAR(100),
    birth_date DATE,
    nationality VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_slug (slug),
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

### **4. books_book_authors** (Many-to-Many)

```sql
CREATE TABLE books_book_authors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    author_id INT NOT NULL,
    
    FOREIGN KEY (book_id) REFERENCES books_book(id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES books_author(id) ON DELETE CASCADE,
    
    UNIQUE KEY unique_book_author (book_id, author_id),
    INDEX idx_book (book_id),
    INDEX idx_author (author_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

### **5. orders_order**

```sql
CREATE TABLE orders_order (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_number VARCHAR(20) UNIQUE NOT NULL,
    user_id INT,
    billing_name VARCHAR(200) NOT NULL,
    billing_email VARCHAR(254) NOT NULL,
    billing_phone VARCHAR(20) NOT NULL,
    billing_address TEXT NOT NULL,
    billing_city VARCHAR(100) NOT NULL,
    billing_postal_code VARCHAR(10),
    shipping_name VARCHAR(200) NOT NULL,
    shipping_phone VARCHAR(20) NOT NULL,
    shipping_address TEXT NOT NULL,
    shipping_city VARCHAR(100) NOT NULL,
    shipping_postal_code VARCHAR(10),
    subtotal DECIMAL(10,2) NOT NULL,
    discount DECIMAL(10,2) DEFAULT 0,
    shipping_cost DECIMAL(10,2) DEFAULT 0,
    total DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    customer_notes TEXT,
    admin_notes TEXT,
    coupon_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    confirmed_at DATETIME,
    shipped_at DATETIME,
    delivered_at DATETIME,
    
    FOREIGN KEY (user_id) REFERENCES accounts_user(id) ON DELETE SET NULL,
    FOREIGN KEY (coupon_id) REFERENCES coupons_coupon(id) ON DELETE SET NULL,
    
    INDEX idx_order_number (order_number),
    INDEX idx_user (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Constraints:**
- `order_number` UNIQUE
- `payment_method` CHECK IN ('online', 'cash')
- `status` CHECK IN ('pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled', 'refunded')

---

### **6. payments_payment**

```sql
CREATE TABLE payments_payment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    transaction_id VARCHAR(100) UNIQUE NOT NULL,
    millipay_order_id VARCHAR(100),
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'AZN',
    status VARCHAR(20) DEFAULT 'pending',
    card_mask VARCHAR(20),
    card_type VARCHAR(20),
    response_data JSON,
    error_message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    
    FOREIGN KEY (order_id) REFERENCES orders_order(id) ON DELETE CASCADE,
    
    INDEX idx_transaction_id (transaction_id),
    INDEX idx_order (order_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Constraints:**
- `transaction_id` UNIQUE
- `status` CHECK IN ('pending', 'processing', 'completed', 'failed', 'refunded')

---

### **7. delivery_delivery**

```sql
CREATE TABLE delivery_delivery (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT UNIQUE NOT NULL,
    courier_id INT,
    tracking_number VARCHAR(50) UNIQUE NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    estimated_delivery_date DATE,
    estimated_delivery_time TIME,
    delivered_at DATETIME,
    delivered_to VARCHAR(200),
    signature VARCHAR(100),
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (order_id) REFERENCES orders_order(id) ON DELETE CASCADE,
    FOREIGN KEY (courier_id) REFERENCES delivery_courier(id) ON DELETE SET NULL,
    
    INDEX idx_tracking_number (tracking_number),
    INDEX idx_order (order_id),
    INDEX idx_courier (courier_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Constraints:**
- `tracking_number` UNIQUE
- `order_id` UNIQUE (1:1 relationship)
- `status` CHECK IN ('pending', 'assigned', 'picked_up', 'in_transit', 'delivered', 'failed')

---

### **8. reviews_review**

```sql
CREATE TABLE reviews_review (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    user_id INT NOT NULL,
    rating INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    is_approved BOOLEAN DEFAULT FALSE,
    is_verified_purchase BOOLEAN DEFAULT FALSE,
    helpful_count INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (book_id) REFERENCES books_book(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES accounts_user(id) ON DELETE CASCADE,
    
    UNIQUE KEY unique_book_user (book_id, user_id),
    INDEX idx_book (book_id),
    INDEX idx_user (user_id),
    INDEX idx_rating (rating),
    INDEX idx_is_approved (is_approved),
    INDEX idx_created_at (created_at DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Constraints:**
- `rating` CHECK BETWEEN 1 AND 5
- UNIQUE (book_id, user_id) - One review per user per book

---

### **9. coupons_coupon**

```sql
CREATE TABLE coupons_coupon (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    discount_type VARCHAR(20) NOT NULL,
    discount_value DECIMAL(10,2) NOT NULL,
    min_purchase_amount DECIMAL(10,2),
    max_discount_amount DECIMAL(10,2),
    usage_limit INT,
    usage_limit_per_user INT DEFAULT 1,
    usage_count INT DEFAULT 0,
    valid_from DATETIME NOT NULL,
    valid_until DATETIME NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_code (code),
    INDEX idx_is_active (is_active),
    INDEX idx_valid_dates (valid_from, valid_until)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Constraints:**
- `code` UNIQUE
- `discount_type` CHECK IN ('percentage', 'fixed')
- `discount_value` > 0

---

## 🔗 Relationships Summary

| Relationship Type | Tables | Cardinality |
|-------------------|--------|-------------|
| **One-to-One** | User ↔ UserProfile | 1:1 |
| **One-to-One** | Order ↔ Delivery | 1:1 |
| **One-to-Many** | User → Orders | 1:N |
| **One-to-Many** | User → Reviews | 1:N |
| **One-to-Many** | User → Wishlist | 1:N |
| **One-to-Many** | Book → Reviews | 1:N |
| **One-to-Many** | Book → OrderItems | 1:N |
| **One-to-Many** | Order → OrderItems | 1:N |
| **One-to-Many** | Order → Payments | 1:N |
| **One-to-Many** | Courier → Deliveries | 1:N |
| **One-to-Many** | Delivery → StatusUpdates | 1:N |
| **One-to-Many** | Coupon → CouponUsages | 1:N |
| **Many-to-Many** | Book ↔ Authors | M:N |
| **Many-to-Many** | Book ↔ Categories | M:N |

---

## 📈 Indexes Strategy

### **Performance Indexes:**

```sql
-- Book search optimization
CREATE FULLTEXT INDEX idx_book_search ON books_book(title, description);

-- Order lookup optimization
CREATE INDEX idx_order_user_status ON orders_order(user_id, status);

-- Review filtering
CREATE INDEX idx_review_book_approved ON reviews_review(book_id, is_approved);

-- Delivery tracking
CREATE INDEX idx_delivery_courier_status ON delivery_delivery(courier_id, status);
```

---

## 🎯 Data Integrity Rules

### **Cascading Deletes:**
- Book deleted → Reviews, OrderItems, CartItems, Wishlist deleted
- Order deleted → OrderItems, Payments, Delivery deleted
- User deleted → Set NULL on Orders, Reviews deleted

### **Constraints:**
- All prices >= 0
- Stock >= 0
- Rating between 1-5
- Discount value > 0
- Order total = subtotal - discount + shipping_cost

---

## 📊 Sample Queries

### **Get bestselling books:**
```sql
SELECT b.*, COUNT(oi.id) as order_count
FROM books_book b
LEFT JOIN orders_orderitem oi ON b.id = oi.book_id
WHERE b.is_active = TRUE
GROUP BY b.id
ORDER BY order_count DESC
LIMIT 10;
```

### **Get user's order history:**
```sql
SELECT o.*, COUNT(oi.id) as item_count
FROM orders_order o
LEFT JOIN orders_orderitem oi ON o.id = oi.order_id
WHERE o.user_id = ?
GROUP BY o.id
ORDER BY o.created_at DESC;
```

### **Get book average rating:**
```sql
SELECT b.*, AVG(r.rating) as avg_rating, COUNT(r.id) as review_count
FROM books_book b
LEFT JOIN reviews_review r ON b.id = r.book_id AND r.is_approved = TRUE
WHERE b.id = ?
GROUP BY b.id;
```

---

## 🔄 Migration Strategy

### **Initial Migration:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **Data Migration Example:**
```python
# migrations/0002_populate_categories.py
from django.db import migrations

def populate_categories(apps, schema_editor):
    Category = apps.get_model('books', 'Category')
    categories = [
        {'name': 'Fiction', 'slug': 'fiction'},
        {'name': 'Non-Fiction', 'slug': 'non-fiction'},
        # ...
    ]
    for cat in categories:
        Category.objects.create(**cat)

class Migration(migrations.Migration):
    dependencies = [
        ('books', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(populate_categories),
    ]
```

---

## 📝 Backup Strategy

### **Daily Backups:**
```bash
# MySQL dump
mysqldump -u username -p olric_bookstore > backup_$(date +%Y%m%d).sql

# Compress
gzip backup_$(date +%Y%m%d).sql
```

### **Restore:**
```bash
mysql -u username -p olric_bookstore < backup_20260121.sql
```

---

**Sənəd versiyası:** 1.0  
**Son yenilənmə:** 2026-01-21  
**Müəllif:** Olric Bookstore Development Team
