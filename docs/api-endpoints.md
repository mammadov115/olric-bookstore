# 🔌 API Endpoints - Olric Bookstore

## 📋 Ümumi Baxış

Bu sənəd Olric Bookstore layihəsinin REST API endpoints-lərini sənədləşdirir. API-lər Django REST Framework ilə hazırlanıb və lazım olduqda istifadə ediləcək (AJAX requests, gələcək mobile app).

---

## 🎯 Base URL

- **Development:** `http://localhost:8000/api/v1/`
- **Production:** `https://olricbookstore.pythonanywhere.com/api/v1/`

---

## 🔐 Authentication

### **Token Authentication (DRF)**

```http
POST /api/v1/auth/login/
Content-Type: application/json

{
    "username": "user@example.com",
    "password": "password123"
}
```

**Response:**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user": {
        "id": 1,
        "username": "user@example.com",
        "email": "user@example.com",
        "role": "customer"
    }
}
```

### **Using Token:**
```http
GET /api/v1/books/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

---

## 📚 Books API

### **1. List Books**

```http
GET /api/v1/books/
```

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `page_size` (int): Items per page (default: 24)
- `category` (slug): Filter by category
- `author` (slug): Filter by author
- `min_price` (decimal): Minimum price
- `max_price` (decimal): Maximum price
- `search` (string): Search in title, description
- `ordering` (string): Sort field (price, -price, created_at, -created_at)
- `is_featured` (bool): Featured books only
- `is_bestseller` (bool): Bestsellers only

**Example:**
```http
GET /api/v1/books/?category=fiction&min_price=10&max_price=50&ordering=-created_at
```

**Response:**
```json
{
    "count": 150,
    "next": "http://localhost:8000/api/v1/books/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "The Great Gatsby",
            "slug": "the-great-gatsby",
            "isbn": "9780743273565",
            "authors": [
                {
                    "id": 1,
                    "name": "F. Scott Fitzgerald",
                    "slug": "f-scott-fitzgerald"
                }
            ],
            "publisher": {
                "id": 1,
                "name": "Scribner",
                "slug": "scribner"
            },
            "categories": [
                {
                    "id": 1,
                    "name": "Fiction",
                    "slug": "fiction"
                }
            ],
            "description": "The story of the mysteriously wealthy Jay Gatsby...",
            "price": "29.99",
            "discount_price": "24.99",
            "final_price": "24.99",
            "stock": 15,
            "cover_image": "http://localhost:8000/media/books/covers/gatsby.jpg",
            "rating": 4.5,
            "review_count": 120,
            "is_in_stock": true,
            "created_at": "2026-01-15T10:30:00Z"
        }
    ]
}
```

---

### **2. Get Book Detail**

```http
GET /api/v1/books/{slug}/
```

**Response:**
```json
{
    "id": 1,
    "title": "The Great Gatsby",
    "slug": "the-great-gatsby",
    "subtitle": "",
    "isbn": "9780743273565",
    "isbn10": "0743273567",
    "authors": [...],
    "publisher": {...},
    "categories": [...],
    "description": "...",
    "table_of_contents": "...",
    "publication_date": "2004-09-30",
    "language": "en",
    "pages": 180,
    "format": "paperback",
    "price": "29.99",
    "discount_price": "24.99",
    "final_price": "24.99",
    "stock": 15,
    "cover_image": "...",
    "images": [
        {
            "id": 1,
            "image": "...",
            "caption": "Back cover"
        }
    ],
    "rating": 4.5,
    "review_count": 120,
    "reviews": [...],
    "is_in_stock": true,
    "views_count": 1250,
    "sales_count": 45,
    "created_at": "2026-01-15T10:30:00Z"
}
```

---

### **3. Search Books**

```http
GET /api/v1/books/search/?q=gatsby
```

**Response:**
```json
{
    "results": [
        {
            "id": 1,
            "title": "The Great Gatsby",
            "slug": "the-great-gatsby",
            "authors": ["F. Scott Fitzgerald"],
            "price": "29.99",
            "cover_image": "..."
        }
    ]
}
```

---

## 🛒 Cart API

### **1. Get Cart**

```http
GET /api/v1/cart/
Authorization: Token {token}
```

**Response:**
```json
{
    "id": 1,
    "items": [
        {
            "id": 1,
            "book": {
                "id": 1,
                "title": "The Great Gatsby",
                "slug": "the-great-gatsby",
                "price": "29.99",
                "cover_image": "..."
            },
            "quantity": 2,
            "price": "29.99",
            "subtotal": "59.98"
        }
    ],
    "subtotal": "59.98",
    "item_count": 2
}
```

---

### **2. Add to Cart**

```http
POST /api/v1/cart/add/
Authorization: Token {token}
Content-Type: application/json

{
    "book_id": 1,
    "quantity": 1
}
```

**Response:**
```json
{
    "message": "Kitab səbətə əlavə edildi",
    "cart": {
        "id": 1,
        "item_count": 3,
        "subtotal": "89.97"
    }
}
```

---

### **3. Update Cart Item**

```http
PATCH /api/v1/cart/items/{item_id}/
Authorization: Token {token}
Content-Type: application/json

{
    "quantity": 3
}
```

**Response:**
```json
{
    "message": "Səbət yeniləndi",
    "item": {
        "id": 1,
        "quantity": 3,
        "subtotal": "89.97"
    }
}
```

---

### **4. Remove from Cart**

```http
DELETE /api/v1/cart/items/{item_id}/
Authorization: Token {token}
```

**Response:**
```json
{
    "message": "Kitab səbətdən silindi"
}
```

---

## 📦 Orders API

### **1. Create Order**

```http
POST /api/v1/orders/
Authorization: Token {token}
Content-Type: application/json

{
    "billing_name": "Elvin Mammadov",
    "billing_email": "elvin@example.com",
    "billing_phone": "+994501234567",
    "billing_address": "Nizami küç. 123",
    "billing_city": "Bakı",
    "billing_postal_code": "AZ1000",
    "shipping_name": "Elvin Mammadov",
    "shipping_phone": "+994501234567",
    "shipping_address": "Nizami küç. 123",
    "shipping_city": "Bakı",
    "shipping_postal_code": "AZ1000",
    "payment_method": "online",
    "coupon_code": "WELCOME10",
    "customer_notes": "Zəhmət olmasa axşam çatdırın"
}
```

**Response:**
```json
{
    "order_number": "ORD-20260121-0001",
    "status": "pending",
    "subtotal": "89.97",
    "discount": "8.99",
    "shipping_cost": "5.00",
    "total": "85.98",
    "payment_url": "https://millipay.az/payment/abc123",
    "created_at": "2026-01-21T14:30:00Z"
}
```

---

### **2. Get Order Detail**

```http
GET /api/v1/orders/{order_number}/
Authorization: Token {token}
```

**Response:**
```json
{
    "order_number": "ORD-20260121-0001",
    "status": "confirmed",
    "items": [
        {
            "book_title": "The Great Gatsby",
            "book_isbn": "9780743273565",
            "quantity": 2,
            "price": "29.99",
            "subtotal": "59.98"
        }
    ],
    "subtotal": "89.97",
    "discount": "8.99",
    "shipping_cost": "5.00",
    "total": "85.98",
    "payment_method": "online",
    "payment_status": "completed",
    "delivery": {
        "tracking_number": "TRK-20260121-0001",
        "status": "in_transit",
        "estimated_delivery_date": "2026-01-23"
    },
    "created_at": "2026-01-21T14:30:00Z",
    "confirmed_at": "2026-01-21T14:35:00Z"
}
```

---

### **3. List User Orders**

```http
GET /api/v1/orders/
Authorization: Token {token}
```

**Response:**
```json
{
    "count": 5,
    "results": [
        {
            "order_number": "ORD-20260121-0001",
            "status": "delivered",
            "total": "85.98",
            "item_count": 3,
            "created_at": "2026-01-21T14:30:00Z"
        }
    ]
}
```

---

## 💳 Payment API

### **1. Initiate Payment**

```http
POST /api/v1/payments/initiate/
Authorization: Token {token}
Content-Type: application/json

{
    "order_number": "ORD-20260121-0001"
}
```

**Response:**
```json
{
    "payment_url": "https://millipay.az/payment/abc123",
    "transaction_id": "TXN-20260121-0001"
}
```

---

### **2. Payment Callback (MilliÖn)**

```http
POST /api/v1/payments/callback/
Content-Type: application/json

{
    "transaction_id": "TXN-20260121-0001",
    "status": "success",
    "amount": "85.98",
    "signature": "..."
}
```

**Response:**
```json
{
    "status": "ok"
}
```

---

## 🚚 Delivery Tracking API

### **1. Track Delivery**

```http
GET /api/v1/delivery/track/{tracking_number}/
```

**Response:**
```json
{
    "tracking_number": "TRK-20260121-0001",
    "order_number": "ORD-20260121-0001",
    "status": "in_transit",
    "courier": {
        "name": "Rəşad Əliyev",
        "phone": "+994501234567",
        "current_location": {
            "lat": 40.4093,
            "lng": 49.8671
        }
    },
    "estimated_delivery_date": "2026-01-23",
    "estimated_delivery_time": "18:00",
    "status_history": [
        {
            "status": "pending",
            "location": "Warehouse",
            "timestamp": "2026-01-21T14:35:00Z"
        },
        {
            "status": "picked_up",
            "location": "Warehouse",
            "timestamp": "2026-01-21T15:00:00Z"
        },
        {
            "status": "in_transit",
            "location": "Nizami District",
            "timestamp": "2026-01-21T16:30:00Z"
        }
    ]
}
```

---

### **2. Update Delivery Location (Courier)**

```http
POST /api/v1/delivery/update-location/
Authorization: Token {courier_token}
Content-Type: application/json

{
    "tracking_number": "TRK-20260121-0001",
    "latitude": 40.4093,
    "longitude": 49.8671,
    "status": "in_transit",
    "notes": "Müştəriyə yaxınlaşıram"
}
```

**Response:**
```json
{
    "message": "Məlumat yeniləndi"
}
```

---

## ⭐ Reviews API

### **1. List Book Reviews**

```http
GET /api/v1/books/{slug}/reviews/
```

**Query Parameters:**
- `page` (int): Page number
- `rating` (int): Filter by rating (1-5)

**Response:**
```json
{
    "count": 120,
    "average_rating": 4.5,
    "rating_distribution": {
        "5": 60,
        "4": 40,
        "3": 15,
        "2": 3,
        "1": 2
    },
    "results": [
        {
            "id": 1,
            "user": {
                "name": "Elvin M.",
                "avatar": "..."
            },
            "rating": 5,
            "title": "Əla kitab!",
            "content": "Çox bəyəndim, hər kəsə tövsiyə edirəm...",
            "is_verified_purchase": true,
            "helpful_count": 15,
            "created_at": "2026-01-20T10:00:00Z"
        }
    ]
}
```

---

### **2. Create Review**

```http
POST /api/v1/books/{slug}/reviews/
Authorization: Token {token}
Content-Type: application/json

{
    "rating": 5,
    "title": "Əla kitab!",
    "content": "Çox bəyəndim, hər kəsə tövsiyə edirəm..."
}
```

**Response:**
```json
{
    "message": "Rəyiniz moderasiyaya göndərildi",
    "review": {
        "id": 121,
        "rating": 5,
        "title": "Əla kitab!",
        "is_approved": false
    }
}
```

---

### **3. Mark Review as Helpful**

```http
POST /api/v1/reviews/{review_id}/helpful/
Authorization: Token {token}
```

**Response:**
```json
{
    "message": "Təşəkkürlər!",
    "helpful_count": 16
}
```

---

## ❤️ Wishlist API

### **1. Get Wishlist**

```http
GET /api/v1/wishlist/
Authorization: Token {token}
```

**Response:**
```json
{
    "count": 5,
    "items": [
        {
            "id": 1,
            "book": {
                "id": 1,
                "title": "The Great Gatsby",
                "slug": "the-great-gatsby",
                "price": "29.99",
                "cover_image": "...",
                "is_in_stock": true
            },
            "added_at": "2026-01-20T10:00:00Z"
        }
    ]
}
```

---

### **2. Add to Wishlist**

```http
POST /api/v1/wishlist/add/
Authorization: Token {token}
Content-Type: application/json

{
    "book_id": 1
}
```

**Response:**
```json
{
    "message": "Kitab istək siyahısına əlavə edildi"
}
```

---

### **3. Remove from Wishlist**

```http
DELETE /api/v1/wishlist/{item_id}/
Authorization: Token {token}
```

**Response:**
```json
{
    "message": "Kitab istək siyahısından silindi"
}
```

---

## 🎟️ Coupons API

### **1. Validate Coupon**

```http
POST /api/v1/coupons/validate/
Authorization: Token {token}
Content-Type: application/json

{
    "code": "WELCOME10",
    "cart_total": "89.97"
}
```

**Response (Valid):**
```json
{
    "valid": true,
    "code": "WELCOME10",
    "discount_type": "percentage",
    "discount_value": "10.00",
    "discount_amount": "8.99",
    "final_total": "81.98"
}
```

**Response (Invalid):**
```json
{
    "valid": false,
    "error": "Kupon müddəti bitib"
}
```

---

## 📊 Dashboard API (Admin)

### **1. Get Dashboard Stats**

```http
GET /api/v1/dashboard/stats/
Authorization: Token {admin_token}
```

**Response:**
```json
{
    "today": {
        "orders": 15,
        "revenue": "1250.00",
        "new_customers": 5
    },
    "this_month": {
        "orders": 450,
        "revenue": "35000.00",
        "new_customers": 120
    },
    "bestsellers": [
        {
            "book": "The Great Gatsby",
            "sales": 45
        }
    ],
    "pending_orders": 8,
    "pending_reviews": 12,
    "low_stock_books": 5
}
```

---

## 🔔 Notifications API

### **1. Get User Notifications**

```http
GET /api/v1/notifications/
Authorization: Token {token}
```

**Response:**
```json
{
    "unread_count": 3,
    "notifications": [
        {
            "id": 1,
            "type": "order_shipped",
            "title": "Sifarişiniz göndərildi",
            "message": "ORD-20260121-0001 nömrəli sifarişiniz göndərildi",
            "is_read": false,
            "created_at": "2026-01-21T16:00:00Z"
        }
    ]
}
```

---

## ⚠️ Error Responses

### **400 Bad Request**
```json
{
    "error": "Validation error",
    "details": {
        "email": ["Bu email artıq istifadə olunub"]
    }
}
```

### **401 Unauthorized**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### **404 Not Found**
```json
{
    "detail": "Not found."
}
```

### **500 Internal Server Error**
```json
{
    "error": "Internal server error",
    "message": "Xəta baş verdi, zəhmət olmasa yenidən cəhd edin"
}
```

---

## 📝 Rate Limiting

- **Anonymous users:** 100 requests/hour
- **Authenticated users:** 1000 requests/hour
- **Admin users:** Unlimited

**Rate Limit Headers:**
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 950
X-RateLimit-Reset: 1642857600
```

---

## 🔒 CORS Configuration

**Allowed Origins (Production):**
- `https://olricbookstore.pythonanywhere.com`
- `https://www.olricbookstore.com`

**Allowed Methods:**
- GET, POST, PUT, PATCH, DELETE, OPTIONS

---

## 📚 API Versioning

Current version: **v1**

Future versions will be accessible via:
- `/api/v2/`
- `/api/v3/`

---

**Sənəd versiyası:** 1.0  
**Son yenilənmə:** 2026-01-21  
**Müəllif:** Olric Bookstore Development Team
