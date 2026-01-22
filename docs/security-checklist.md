# 🔒 Security Checklist - Olric Bookstore

## 📋 Ümumi Baxış

Bu sənəd Olric Bookstore layihəsinin təhlükəsizlik tələblərini və yoxlama siyahısını əhatə edir. Hər bir deployment-dən əvvəl bu checklist-i yoxlamaq vacibdir.

---

## 🎯 Security Principles

### **1. Defense in Depth**
Bir neçə təhlükəsizlik layerı istifadə et

### **2. Least Privilege**
Minimum lazımi icazələr ver

### **3. Fail Securely**
Xəta zamanı təhlükəsiz state-ə keç

### **4. Never Trust User Input**
Bütün user input-ları validate et

---

## ✅ Django Security Checklist

### **1. Settings Configuration**

```python
# ✅ Production settings
DEBUG = False
ALLOWED_HOSTS = ['olricbookstore.pythonanywhere.com', 'www.olricbookstore.com']

# ✅ Secret key
SECRET_KEY = os.getenv('SECRET_KEY')  # Never hardcode!

# ✅ Security headers
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ✅ Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

**Checklist:**
- [ ] `DEBUG = False` in production
- [ ] `SECRET_KEY` environment variable-dan oxunur
- [ ] `ALLOWED_HOSTS` düzgün konfiqurasiya olunub
- [ ] SSL/HTTPS redirect aktiv
- [ ] Secure cookies aktiv
- [ ] Security headers konfiqurasiya olunub
- [ ] Password validators aktiv

---

### **2. CSRF Protection**

```python
# ✅ CSRF middleware aktiv
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection
    # ...
]

# ✅ CSRF cookie settings
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Strict'
```

**Templates:**
```django
{# ✅ CSRF token hər formda #}
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

**AJAX:**
```javascript
// ✅ CSRF token AJAX request-lərdə
$.ajax({
    url: '/api/endpoint/',
    method: 'POST',
    headers: {
        'X-CSRFToken': getCookie('csrftoken')
    },
    data: {...}
});
```

**Checklist:**
- [ ] CSRF middleware aktiv
- [ ] Bütün formlarda `{% csrf_token %}`
- [ ] AJAX requests-də CSRF token
- [ ] CSRF cookie secure settings

---

### **3. XSS Protection**

```python
# ✅ Auto-escaping aktiv (Django default)
# Templates automatically escape HTML

# ⚠️ Safe filter yalnız trusted content üçün
{{ user_input }}  # ✅ Auto-escaped
{{ trusted_html|safe }}  # ⚠️ Only for trusted content
```

**Input Sanitization:**
```python
# ✅ Clean user input
from django.utils.html import escape, strip_tags

def clean_user_input(text):
    """Remove HTML tags and escape special characters."""
    text = strip_tags(text)
    text = escape(text)
    return text
```

**Checklist:**
- [ ] Auto-escaping aktiv
- [ ] `|safe` filter yalnız trusted content üçün
- [ ] User input sanitization
- [ ] Rich text editor-da HTML sanitization (bleach library)

---

### **4. SQL Injection Protection**

```python
# ✅ DÜZGÜN - ORM istifadə et
books = Book.objects.filter(title__icontains=search_query)

# ❌ YANLIŞ - Raw SQL
cursor.execute(f"SELECT * FROM books WHERE title LIKE '%{search_query}%'")

# ✅ Əgər raw SQL lazımdırsa, parameterized queries
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT * FROM books WHERE title LIKE %s", [f'%{search_query}%'])
```

**Checklist:**
- [ ] Django ORM istifadə olunur
- [ ] Raw SQL minimuma endirilir
- [ ] Raw SQL-də parameterized queries
- [ ] No string interpolation in SQL

---

### **5. Authentication & Authorization**

```python
# ✅ Strong password hashing
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# ✅ Session security
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_AGE = 86400  # 24 hours

# ✅ Login attempt limiting
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1  # 1 hour
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True
```

**Views:**
```python
# ✅ Login required decorator
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    return render(request, 'profile.html')

# ✅ Permission required
from django.contrib.auth.decorators import permission_required

@permission_required('books.add_book')
def add_book_view(request):
    # ...
```

**Checklist:**
- [ ] Strong password hashers
- [ ] Password validators aktiv
- [ ] Session security konfiqurasiya
- [ ] Login attempt limiting (django-axes)
- [ ] `@login_required` decorator istifadə
- [ ] Permission checks
- [ ] Two-factor authentication (gələcək)

---

### **6. Rate Limiting**

```python
# ✅ django-ratelimit
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', method='POST')
def login_view(request):
    # Login logic
    pass

@ratelimit(key='user', rate='100/h')
def api_view(request):
    # API logic
    pass
```

**Settings:**
```python
# ✅ Rate limit configuration
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'
```

**Checklist:**
- [ ] django-ratelimit və ya django-axes installed
- [ ] Login endpoint rate limited
- [ ] API endpoints rate limited
- [ ] Registration endpoint rate limited
- [ ] Password reset rate limited

---

### **7. File Upload Security**

```python
# ✅ File upload validation
from django.core.validators import FileExtensionValidator

class Book(models.Model):
    cover_image = models.ImageField(
        upload_to='books/covers/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

# ✅ File size limit
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB

def validate_file_size(file):
    if file.size > MAX_UPLOAD_SIZE:
        raise ValidationError('File too large. Max size is 5MB.')
```

**Settings:**
```python
# ✅ Media files configuration
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# ✅ File upload handlers
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
```

**Checklist:**
- [ ] File extension validation
- [ ] File size limits
- [ ] Image validation (Pillow)
- [ ] Virus scanning (ClamAV - gələcək)
- [ ] Media files CDN-də serve olunur

---

### **8. Payment Security**

```python
# ✅ PCI DSS Compliance

# ❌ HEÇVAXT card məlumatları database-də saxlama!
# ✅ MilliÖn payment gateway istifadə et

class Payment(models.Model):
    # ✅ Yalnız masked card number
    card_mask = models.CharField(max_length=20)  # "****1234"
    card_type = models.CharField(max_length=20)  # "Visa"
    
    # ❌ YANLIŞ - Full card details
    # card_number = models.CharField(max_length=16)  # NEVER!
    # cvv = models.CharField(max_length=3)  # NEVER!
```

**MilliÖn Integration:**
```python
# ✅ Signature verification
def verify_millipay_signature(data, signature):
    """Verify MilliÖn callback signature."""
    expected_signature = hmac.new(
        settings.MILLIPAY_SECRET_KEY.encode(),
        json.dumps(data).encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected_signature)
```

**Checklist:**
- [ ] Heç vaxt card details database-də saxlanılmır
- [ ] Payment gateway (MilliÖn) istifadə olunur
- [ ] Webhook signature verification
- [ ] HTTPS only for payment pages
- [ ] Payment logs encrypted
- [ ] PCI DSS compliance

---

### **9. API Security**

```python
# ✅ Token authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}
```

**CORS Configuration:**
```python
# ✅ CORS headers
CORS_ALLOWED_ORIGINS = [
    'https://olricbookstore.pythonanywhere.com',
    'https://www.olricbookstore.com',
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
]
```

**Checklist:**
- [ ] Token authentication aktiv
- [ ] API rate limiting
- [ ] CORS düzgün konfiqurasiya
- [ ] API versioning
- [ ] Input validation
- [ ] Error messages məlumat sızdırmır

---

### **10. Database Security**

```python
# ✅ Database credentials environment variables-da
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    }
}
```

**Backup Strategy:**
```bash
# ✅ Daily automated backups
0 3 * * * mysqldump -u user -p'password' dbname | gzip > ~/backups/db_$(date +\%Y\%m\%d).sql.gz

# ✅ Backup retention (30 days)
find ~/backups/ -name "db_*.sql.gz" -mtime +30 -delete
```

**Checklist:**
- [ ] Database credentials environment variables-da
- [ ] Strong database password
- [ ] Database user minimal permissions
- [ ] Daily automated backups
- [ ] Backup encryption
- [ ] Backup testing (restore test)
- [ ] Database connection over SSL (production)

---

### **11. Logging & Monitoring**

```python
# ✅ Security event logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/olricbookstore/security.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}
```

**Security Events to Log:**
- Failed login attempts
- Permission denied
- CSRF failures
- Suspicious activities
- Payment transactions
- Admin actions

**Checklist:**
- [ ] Security logging konfiqurasiya
- [ ] Failed login attempts log olunur
- [ ] Suspicious activities monitor olunur
- [ ] Log files secure location-da
- [ ] Log rotation konfiqurasiya
- [ ] Sentry və ya digər error tracking

---

### **12. Third-Party Dependencies**

```bash
# ✅ Dependency security check with Poetry
poetry add --group dev safety
poetry run safety check

# ✅ Check for outdated packages
poetry show --outdated

# ✅ Update dependencies
poetry update

# ✅ Update specific package
poetry update django
```

**pyproject.toml:**
```toml
[tool.poetry.dependencies]
# ✅ Pin versions with caret (^) - allows minor updates
Django = "^5.0.1"  # Allows 5.0.x, 5.1.x but not 6.0.0
djangorestframework = "^3.14.0"

# ✅ Or use exact version
Pillow = "10.1.0"
```

**Checklist:**
- [ ] Bütün dependencies version-pinned (pyproject.toml)
- [ ] Regular security updates (`poetry update`)
- [ ] `poetry run safety check` run olunur
- [ ] Vulnerable packages yoxdur
- [ ] Unused dependencies remove olunub (`poetry remove`)

---

### **13. Environment Variables**

```python
# ✅ python-decouple istifadə et
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
DATABASE_URL = config('DATABASE_URL')
```

**.env file:**
```env
# ✅ Never commit to git!
SECRET_KEY=super-secret-key-here
DEBUG=False
DATABASE_URL=mysql://user:pass@host/db
MILLIPAY_SECRET_KEY=secret
```

**.gitignore:**
```
# ✅ Ignore sensitive files
.env
*.log
*.pyc
__pycache__/
db.sqlite3
media/
```

**Checklist:**
- [ ] `.env` file istifadə olunur
- [ ] `.env` gitignore-da
- [ ] `.env.example` provided
- [ ] No hardcoded secrets
- [ ] Environment-specific settings

---

### **14. Admin Panel Security**

```python
# ✅ Custom admin URL
# urls.py
urlpatterns = [
    path('secret-admin-panel-xyz/', admin.site.urls),  # Not /admin/
]

# ✅ Admin IP whitelist (optional)
ALLOWED_ADMIN_IPS = ['123.456.789.0']

class AdminIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.path.startswith('/secret-admin-panel-xyz/'):
            ip = request.META.get('REMOTE_ADDR')
            if ip not in settings.ALLOWED_ADMIN_IPS:
                raise PermissionDenied
        return self.get_response(request)
```

**Checklist:**
- [ ] Admin URL custom (not /admin/)
- [ ] Admin login rate limited
- [ ] Strong admin passwords
- [ ] Admin IP whitelist (optional)
- [ ] Admin actions logged
- [ ] Two-factor authentication (gələcək)

---

### **15. Error Handling**

```python
# ✅ Custom error pages
# views.py
def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    return render(request, 'errors/500.html', status=500)

# urls.py
handler404 = 'myapp.views.handler404'
handler500 = 'myapp.views.handler500'
```

**Error Messages:**
```python
# ✅ DÜZGÜN - Generic error
raise ValidationError("Invalid input")

# ❌ YANLIŞ - Too much information
raise ValidationError(f"User {username} not found in database table users")
```

**Checklist:**
- [ ] Custom error pages (404, 500)
- [ ] Generic error messages (no sensitive info)
- [ ] Error logging (Sentry)
- [ ] `DEBUG = False` in production
- [ ] No stack traces to users

---

## 🔍 Security Testing

### **1. Penetration Testing Checklist**

- [ ] SQL Injection testing
- [ ] XSS testing
- [ ] CSRF testing
- [ ] Authentication bypass testing
- [ ] Authorization testing
- [ ] Session management testing
- [ ] File upload testing
- [ ] API security testing

### **2. Automated Security Scanning**

```bash
# ✅ Django security check
python manage.py check --deploy

# ✅ Bandit (Python security linter)
pip install bandit
bandit -r .

# ✅ Safety (dependency vulnerabilities)
pip install safety
safety check

# ✅ OWASP ZAP (web app scanner)
# Download and run against staging environment
```

---

## 📋 Pre-Deployment Security Checklist

### **Critical (Must Have):**
- [ ] `DEBUG = False`
- [ ] `SECRET_KEY` is secret and strong
- [ ] `ALLOWED_HOSTS` configured
- [ ] HTTPS/SSL enabled
- [ ] CSRF protection aktiv
- [ ] XSS protection aktiv
- [ ] SQL injection protection (ORM)
- [ ] Strong password validation
- [ ] Secure cookies
- [ ] Rate limiting
- [ ] File upload validation
- [ ] Payment security (PCI DSS)
- [ ] Database credentials secure
- [ ] `.env` file not in git
- [ ] Error logging configured

### **Important (Should Have):**
- [ ] Login attempt limiting
- [ ] Admin panel secured
- [ ] API authentication
- [ ] CORS configured
- [ ] Security headers
- [ ] Dependency security check
- [ ] Backup strategy
- [ ] Monitoring configured

### **Nice to Have (Future):**
- [ ] Two-factor authentication
- [ ] IP whitelisting
- [ ] Virus scanning
- [ ] WAF (Web Application Firewall)
- [ ] DDoS protection
- [ ] Security audit

---

## 🚨 Incident Response Plan

### **1. Security Breach Detection**
- Monitor error logs
- Check for suspicious activities
- Review access logs

### **2. Immediate Actions**
1. Isolate affected systems
2. Change all passwords and tokens
3. Notify users if data compromised
4. Document incident

### **3. Recovery**
1. Patch vulnerabilities
2. Restore from backups if needed
3. Review and improve security

### **4. Post-Incident**
1. Conduct security audit
2. Update security policies
3. Train team on lessons learned

---

## 📚 Security Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security](https://docs.djangoproject.com/en/5.0/topics/security/)
- [PCI DSS Compliance](https://www.pcisecuritystandards.org/)
- [CWE Top 25](https://cwe.mitre.org/top25/)

---

**Sənəd versiyası:** 1.0  
**Son yenilənmə:** 2026-01-21  
**Müəllif:** Olric Bookstore Development Team
