# 🛠️ Tech Stack - Olric Bookstore

## 📋 Ümumi Baxış

Bu sənəd Olric Bookstore layihəsində istifadə olunan texnologiyaları və onların seçim səbəblərini ətraflı şəkildə izah edir.

---

## 🎯 Backend

### **Django 5.x**
**Seçim Səbəbi:**
- ✅ Python-un ən populyar və mature web framework-ü
- ✅ "Batteries included" - built-in admin, ORM, authentication
- ✅ Güclü security features (CSRF, XSS, SQL injection protection)
- ✅ Böyük community və geniş documentation
- ✅ Monolith struktur üçün ideal
- ✅ Azərbaycan bazarında developer tapmaq asandır

**İstifadə sahələri:**
- Models, Views, Templates (MVT pattern)
- URL routing
- Form handling və validation
- User authentication və authorization
- Admin panel (custom admin üçün base)

---

### **Django ORM**
**Seçim Səbəbi:**
- ✅ SQL injection-dan qorunma
- ✅ Database-agnostic (MySQL-dən PostgreSQL-ə keçid asandır)
- ✅ Migrations sistemi (database schema versioning)
- ✅ QuerySet API (lazy evaluation, optimization)
- ✅ Raw SQL-ə ehtiyac minimuma enir

**İstifadə sahələri:**
- Database queries
- Model relationships (ForeignKey, ManyToMany)
- Data validation
- Database migrations

---

### **MySQL 8.x**
**Seçim Səbəbi:**
- ✅ PythonAnywhere free plan dəstəkləyir
- ✅ Yüngül və sürətli (kitab mağazası üçün kifayətdir)
- ✅ JSON field support (Django 3.1+)
- ✅ ACID compliance
- ✅ Gələcəkdə PostgreSQL-ə keçid mümkündür

**Gələcək Plan:**
- Production-da PostgreSQL-ə keçid (daha güclü full-text search, JSON operations)

---

### **Django REST Framework (DRF)**
**Seçim Səbəbi:**
- ✅ Lazım olarsa API endpoints yaratmaq üçün
- ✅ Serialization və validation
- ✅ Authentication (Token, JWT)
- ✅ Browsable API (development üçün əla)
- ✅ Throttling və permissions

**İstifadə sahələri:**
- Mobile app üçün API (gələcək)
- AJAX requests (frontend interactions)
- Third-party integrations

---

## 🎨 Frontend

### **Tailwind CSS 3.x (CDN)**
**Seçim Səbəbi:**
- ✅ Utility-first approach (sürətli development)
- ✅ Penguin UK dizaynını tez implement etmək üçün ideal
- ✅ Responsive design out-of-the-box
- ✅ CDN istifadə - No build step lazım deyil
- ✅ Custom admin panel üçün mükəmməl
- ✅ Modern və trendy
- ✅ No Node.js dependency

**İstifadə sahələri:**
- Layout və styling
- Responsive design
- Custom admin panel UI
- Component styling

**CDN Setup:**
```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="az">
<head>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Custom Configuration -->
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        'penguin-orange': '#FF6600',
                        'penguin-navy': '#003B5C',
                        'penguin-yellow': '#FFD700',
                    },
                    fontFamily: {
                        'sans': ['Inter', 'system-ui', 'sans-serif'],
                    }
                }
            }
        }
    </script>
</head>
<body>
    <!-- Content -->
</body>
</html>
```

**Üstünlüklər:**
- ✅ Instant setup (1 dəqiqə)
- ✅ No Node.js required
- ✅ No build process
- ✅ Easy deployment (PythonAnywhere)
- ✅ Hot reload with Django runserver

**Gələcək Optimization (Production):**
```bash
# Lazım olduqda build process-ə keçmək mümkündür
npm install -D tailwindcss
npx tailwindcss -o static/css/output.css --minify
```

---

### **jQuery 3.x**
**Seçim Səbəbi:**
- ✅ Separation of concerns (HTML-dən ayrı JS files)
- ✅ DOM manipulation asandır
- ✅ AJAX requests (simple və straightforward)
- ✅ Browser compatibility
- ✅ Böyük layihələrdə maintainable
- ✅ Alpine.js-dən fərqli olaraq HTML overload yoxdur

**İstifadə sahələri:**
- Form validation (client-side)
- AJAX requests (cart, wishlist, filters)
- Dynamic content loading
- UI interactions (modals, dropdowns, sliders)

**Struktur:**
```
static/
├── js/
│   ├── main.js           # Global functions
│   ├── cart.js           # Shopping cart logic
│   ├── wishlist.js       # Wishlist functionality
│   ├── search.js         # Search & filtering
│   └── checkout.js       # Checkout process
```

---

### **Font Awesome 6.x**
**Seçim Səbəbi:**
- ✅ 10,000+ icons
- ✅ Free plan kifayətdir
- ✅ CDN ilə yüklənir (fast loading)
- ✅ Scalable vector icons
- ✅ Penguin UK dizaynında istifadə üçün uyğun

**İstifadə sahələri:**
- Navigation icons
- Social media icons
- Cart, wishlist, search icons
- Admin panel icons

---

## 🔐 Authentication & Security

### **Django Authentication System**
**Seçim Səbəbi:**
- ✅ Built-in və battle-tested
- ✅ User, Group, Permission models
- ✅ Password hashing (PBKDF2)
- ✅ Session management
- ✅ Login/logout/password reset views

**İstifadə sahələri:**
- User registration və login
- Role-based access (Admin, Kuryer, Müştəri)
- Permission checks
- Session management

---

### **django-ratelimit / django-axes**
**Seçim Səbəbi:**
- ✅ Brute force hücumlarına qarşı
- ✅ Login attempts limiting
- ✅ IP-based blocking
- ✅ Configurable thresholds

**Konfiqurasiya:**
```python
# settings.py
AXES_FAILURE_LIMIT = 5  # 5 failed attempts
AXES_COOLOFF_TIME = 1   # 1 hour block
```

---

## 💳 Payment Integration

### **MilliÖn Payment Gateway**
**Seçim Səbəbi:**
- ✅ Azərbaycanın ən populyar payment aggregator-u
- ✅ Bütün lokal banklar ilə inteqrasiya
- ✅ Visa, Mastercard dəstəyi
- ✅ Yaxşı API documentation
- ✅ Test environment mövcuddur
- ✅ PCI DSS compliant (ödəniş məlumatları bizim serverdə saxlanılmır)

**İstifadə sahələri:**
- Online payments
- Payment callbacks
- Transaction logging
- Refund processing

**Integration Flow:**
```
1. User checkout → Create payment request
2. Redirect to MilliÖn → User enters card details
3. MilliÖn callback → Update order status
4. Webhook → Confirm payment
```

---

## 📦 Deployment & Infrastructure

### **PythonAnywhere**
**Seçim Səbəbi:**
- ✅ Django hosting üçün specialized
- ✅ Free plan test üçün ideal
- ✅ MySQL included
- ✅ SSL/HTTPS support
- ✅ Easy deployment
- ✅ Scheduled tasks (cron jobs)

**Limitlər (Free Plan):**
- ❌ Redis yoxdur (file-based cache istifadə edəcəyik)
- ❌ Background tasks limitlidir
- ❌ CPU time limitlidir

**Gələcək Plan:**
- Production: DigitalOcean, AWS, Heroku

---

### **Docker & Docker Compose**
**Seçim Səbəbi:**
- ✅ Development environment consistency
- ✅ Gələcək deployment üçün hazırlıq
- ✅ Microservices-ə keçid asanlaşır
- ✅ CI/CD pipeline üçün ideal

**Struktur:**
```yaml
# docker-compose.yml
services:
  web:
    build: .
    ports:
      - "8000:8000"
  db:
    image: mysql:8
  redis:  # Gələcək üçün
    image: redis:alpine
```

---

### **Cloudflare CDN**
**Seçim Səbəbi:**
- ✅ Tamamilə PULSUZ
- ✅ Unlimited bandwidth
- ✅ Global CDN (fast loading worldwide)
- ✅ SSL/HTTPS included
- ✅ DDoS protection
- ✅ Auto-minify CSS/JS
- ✅ Caching rules

**İstifadə sahələri:**
- Static files (CSS, JS, images)
- Book cover images
- Performance optimization

---

## 🌍 Internationalization

### **Django i18n**
**Seçim Səbəbi:**
- ✅ Built-in translation framework
- ✅ .po files (easy translation management)
- ✅ Template tags ({% trans %}, {% blocktrans %})
- ✅ Language switching

**Dəstəklənən dillər:**
- 🇦🇿 Azərbaycan dili (default)
- 🇬🇧 İngilis dili

**Struktur:**
```
locale/
├── az/
│   └── LC_MESSAGES/
│       ├── django.po
│       └── django.mo
└── en/
    └── LC_MESSAGES/
        ├── django.po
        └── django.mo
```

---

## 📧 Email & Notifications

### **Django Email Backend**
**Seçim Səbəbi:**
- ✅ Built-in email support
- ✅ SMTP configuration
- ✅ HTML email templates
- ✅ Attachment support

**Email Providers (seçimlər):**
- SendGrid (free tier: 100 emails/day)
- Mailgun (free tier: 5000 emails/month)
- Gmail SMTP (test üçün)

**İstifadə sahələri:**
- Order confirmation
- Shipping updates
- Password reset
- Marketing campaigns

---

### **SMS Gateway (Delivery Tracking)**
**Seçim Səbəbi:**
- Azercell Business SMS
- Bakcell SMS Gateway
- Twilio (xarici, universal)

**İstifadə sahələri:**
- Order status updates
- Delivery notifications
- OTP verification (gələcək)

---

## 📚 External APIs

### **Google Books API**
**Seçim Səbəbi:**
- ✅ Tamamilə PULSUZ (1000 requests/day)
- ✅ Comprehensive book data
- ✅ Book covers, descriptions, ISBNs
- ✅ Author information
- ✅ Easy integration

**İstifadə sahələri:**
- Book data import
- Auto-fill book information
- Book search suggestions

**API Endpoint:**
```
GET https://www.googleapis.com/books/v1/volumes?q=isbn:{ISBN}
```

---

## 🧪 Testing & Quality

### **pytest-django**
**Seçim Səbəbi:**
- ✅ Django TestCase-dən daha güclü
- ✅ Fixtures support
- ✅ Parametrized tests
- ✅ Better assertions
- ✅ Parallel test execution

---

### **coverage.py**
**Seçim Səbəbi:**
- ✅ Code coverage measurement
- ✅ HTML reports
- ✅ Branch coverage
- ✅ Minimum 80% hədəfi

---

### **Faker**
**Seçim Səbəbi:**
- ✅ Realistic fake data generation
- ✅ Localization support (Azərbaycan adları)
- ✅ Development və testing üçün ideal

**İstifadə sahələri:**
- Test data generation
- Database seeding
- Demo data

---

### **factory_boy**
**Seçim Səbəbi:**
- ✅ Model factory pattern
- ✅ Test data creation
- ✅ Faker integration
- ✅ Relationships handling

---

## � Package Management

### **Poetry**
**Seçim Səbəbi:**
- ✅ Modern Python dependency management
- ✅ Deterministic builds (poetry.lock file)
- ✅ Virtual environment avtomatik idarə
- ✅ Dependency resolution daha yaxşıdır
- ✅ `pyproject.toml` - PEP 518 standartı
- ✅ Build və publish asandır
- ✅ Development və production dependencies ayrı

**Installation:**
```bash
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

# Linux/macOS
curl -sSL https://install.python-poetry.org | python3 -
```

**Project Setup:**
```bash
# Initialize new project
poetry init

# Install dependencies
poetry install

# Add dependency
poetry add django
poetry add djangorestframework
poetry add pillow

# Add dev dependency
poetry add --group dev pytest
poetry add --group dev black
poetry add --group dev flake8

# Update dependencies
poetry update

# Show installed packages
poetry show

# Activate virtual environment
poetry shell

# Run command in venv
poetry run python manage.py runserver
```

**pyproject.toml Example:**
```toml
[tool.poetry]
name = "olric-bookstore"
version = "1.0.0"
description = "Online bookstore platform"
authors = ["Olric Team <team@olricbookstore.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.10"
django = "^5.0.1"
djangorestframework = "^3.14.0"
pillow = "^10.1.0"
mysqlclient = "^2.2.0"
python-decouple = "^3.8"
django-cors-headers = "^4.3.1"
django-ratelimit = "^4.1.0"
requests = "^2.31.0"
gunicorn = "^21.2.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.3"
pytest-django = "^4.7.0"
pytest-cov = "^4.1.0"
factory-boy = "^3.3.0"
faker = "^20.1.0"
black = "^23.12.1"
flake8 = "^7.0.0"
django-debug-toolbar = "^4.2.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 100
target-version = ['py310']
include = '\.pyi?$'

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.testing"
python_files = ["tests.py", "test_*.py", "*_tests.py"]
```

**Üstünlükləri:**
- ✅ `requirements.txt`-dən daha güclü
- ✅ Dependency conflicts avtomatik həll olunur
- ✅ Lock file versiyaları sabitləşdirir
- ✅ Monorepo support
- ✅ Plugin system

---

## �🔧 Development Tools

### **Environment Variables (.env)**
**Seçim Səbəbi:**
- ✅ Sensitive data protection
- ✅ Environment-specific configuration
- ✅ 12-factor app methodology

**python-decouple library:**
```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```

**Konfiqurasiya:**
```env
# .env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=mysql://user:pass@localhost/dbname
MILLIPAY_MERCHANT_ID=xxx
MILLIPAY_SECRET_KEY=xxx
EMAIL_HOST_USER=xxx
EMAIL_HOST_PASSWORD=xxx
```

---

## 📊 Monitoring & Logging (Gələcək)

### **Django Debug Toolbar** (Development)
- SQL query analysis
- Template rendering time
- Cache usage

### **Sentry** (Production)
- Error tracking
- Performance monitoring
- Real-time alerts

---

## 🎯 Xülasə

| Kateqoriya | Texnologiya | Səbəb |
|------------|-------------|-------|
| **Backend** | Django 5.x | Mature, secure, batteries-included |
| **Database** | MySQL 8.x | PythonAnywhere support, yüngül |
| **Frontend** | Tailwind CSS | Utility-first, sürətli development |
| **JavaScript** | jQuery 3.x | Separation of concerns, maintainable |
| **Icons** | Font Awesome | 10,000+ icons, free |
| **Payment** | MilliÖn | Azərbaycan bazarı, PCI DSS |
| **Deployment** | PythonAnywhere | Django-friendly, free tier |
| **CDN** | Cloudflare | Pulsuz, unlimited bandwidth |
| **Email** | SendGrid/Mailgun | Free tier, reliable |
| **Testing** | pytest-django | Güclü, modern |
| **Fake Data** | Faker | Realistic test data |

---

## 🚀 Növbəti Addımlar

1. ✅ Virtual environment yaratmaq
2. ✅ Dependencies install (requirements.txt)
3. ✅ Django project initialize
4. ✅ Database setup
5. ✅ Tailwind CSS konfiqurasiya
6. ✅ Docker setup
7. ✅ Git repository initialize

---

**Sənəd versiyası:** 1.0  
**Son yenilənmə:** 2026-01-21  
**Müəllif:** Olric Bookstore Development Team
