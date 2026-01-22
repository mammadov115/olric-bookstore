# 🚀 Deployment Guide - Olric Bookstore

## 📋 Ümumi Baxış

Bu sənəd Olric Bookstore layihəsinin PythonAnywhere-ə deployment prosesini addım-addım izah edir. Həmçinin Docker və gələcək deployment seçimlərini də əhatə edir.

---

## 🎯 Deployment Environments

| Environment | URL | Purpose |
|-------------|-----|---------|
| **Development** | `http://localhost:8000` | Local development |
| **Staging** | `https://staging.olricbookstore.pythonanywhere.com` | Testing (optional) |
| **Production** | `https://olricbookstore.pythonanywhere.com` | Live site |

---

## 📦 Pre-Deployment Checklist

### **1. Code Preparation**

- [ ] All tests passing (`python manage.py test`)
- [ ] Code reviewed and merged to `main` branch
- [ ] No `print()` or `console.log()` statements
- [ ] No hardcoded credentials
- [ ] `.env.example` updated
- [ ] `requirements.txt` updated
- [ ] Migrations created and tested
- [ ] Static files collected locally

### **2. Environment Variables**

Create `.env` file with:

```env
# Django Settings
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=olricbookstore.pythonanywhere.com,www.olricbookstore.com

# Database
DB_NAME=olricbookstore_db
DB_USER=olricbookstore_user
DB_PASSWORD=strong-password-here
DB_HOST=olricbookstore.mysql.pythonanywhere-services.com
DB_PORT=3306

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key

# MilliÖn Payment
MILLIPAY_MERCHANT_ID=your-merchant-id
MILLIPAY_SECRET_KEY=your-secret-key
MILLIPAY_API_URL=https://api.millipay.az/v1/
MILLIPAY_TEST_MODE=False

# Cloudflare CDN
CLOUDFLARE_ZONE_ID=your-zone-id
CLOUDFLARE_API_TOKEN=your-api-token

# SMS Gateway
SMS_GATEWAY_API_KEY=your-sms-api-key
SMS_GATEWAY_SENDER=OlricBooks

# Google Books API
GOOGLE_BOOKS_API_KEY=your-google-books-api-key

# Security
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
```

---

## 🐍 PythonAnywhere Deployment

### **Step 1: Create PythonAnywhere Account**

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for free account
3. Verify email

### **Step 2: Upload Code**

**Option A: Git Clone (Recommended)**

```bash
# SSH into PythonAnywhere console
cd ~
git clone https://github.com/yourusername/olric-bookstore.git
cd olric-bookstore
```

**Option B: Upload ZIP**

1. Compress project locally
2. Upload via Files tab
3. Extract in home directory

### **Step 3: Install Poetry**

```bash
# In PythonAnywhere console
cd ~
curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH (add to ~/.bashrc)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verify installation
poetry --version
```

### **Step 4: Setup Project**

```bash
cd ~/olric-bookstore

# Configure Poetry to create venv in project directory
poetry config virtualenvs.in-project true

# Install dependencies
poetry install --no-root

# Or install without dev dependencies (production)
poetry install --no-root --without dev
```

### **Step 5: Configure Database**

1. Go to **Databases** tab
2. Create MySQL database: `olricbookstore_db`
3. Note down database credentials
4. Create `.env` file with database settings

```bash
# In PythonAnywhere console
cd ~/olric-bookstore
nano .env
# Paste environment variables
# Ctrl+X, Y, Enter to save
```

### **Step 6: Run Migrations**

```bash
cd ~/olric-bookstore

# Run migrations
poetry run python manage.py migrate

# Create superuser
poetry run python manage.py createsuperuser

# Collect static files
poetry run python manage.py collectstatic --noinput

# Load initial data (optional)
poetry run python manage.py loaddata initial_data.json
```

### **Step 7: Configure Web App**

1. Go to **Web** tab
2. Click **Add a new web app**
3. Select **Manual configuration**
4. Choose **Python 3.10**

**WSGI Configuration:**

Click on WSGI configuration file and replace with:

```python
import os
import sys

# Add project directory to sys.path
path = '/home/yourusername/olric-bookstore'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.production'

# Load environment variables from .env
from dotenv import load_dotenv
project_folder = os.path.expanduser('~/olric-bookstore')
load_dotenv(os.path.join(project_folder, '.env'))

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### **Step 8: Configure Static Files**

In **Web** tab, add static files mappings:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/olric-bookstore/staticfiles/` |
| `/media/` | `/home/yourusername/olric-bookstore/media/` |

### **Step 9: Configure Virtual Environment**

In **Web** tab, set virtualenv path:

```
/home/yourusername/olric-bookstore/.venv
```

**Note:** Poetry creates `.venv` directory in project root when `virtualenvs.in-project` is true.

### **Step 10: Reload Web App**

Click **Reload** button in Web tab.

### **Step 11: Test Deployment**

Visit: `https://yourusername.pythonanywhere.com`

---

## 🔧 Post-Deployment Configuration

### **1. Setup Scheduled Tasks**

Go to **Tasks** tab and add:

**Daily Database Backup (3:00 AM):**
```bash
cd ~/olric-bookstore && poetry run python manage.py dbbackup
```

**Clear Expired Sessions (Daily):**
```bash
cd ~/olric-bookstore && poetry run python manage.py clearsessions
```

**Update Book Stats (Hourly):**
```bash
cd ~/olric-bookstore && poetry run python manage.py update_book_stats
```

### **2. Setup Cloudflare CDN**

1. Add domain to Cloudflare
2. Update nameservers
3. Configure SSL (Full Strict)
4. Enable Auto Minify (CSS, JS)
5. Configure caching rules

**Caching Rules:**
- Static files: Cache everything (1 month)
- Media files: Cache everything (1 week)
- HTML: Cache with edge TTL (1 hour)

### **3. Configure Email**

**SendGrid Setup:**

1. Create SendGrid account
2. Verify sender email
3. Create API key
4. Add to `.env`

**Test Email:**
```bash
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'noreply@olricbookstore.com', ['your@email.com'])
```

### **4. Configure MilliÖn Payment**

1. Contact MilliÖn for merchant account
2. Get credentials (merchant_id, secret_key)
3. Add to `.env`
4. Test in sandbox mode first
5. Switch to production mode

---

## 🐳 Docker Deployment (Alternative)

### **Docker Setup**

**Dockerfile:**

```dockerfile
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    volumes:
      - mysql_data:/var/lib/mysql
    environment:
      MYSQL_DATABASE: olricbookstore
      MYSQL_USER: olricuser
      MYSQL_PASSWORD: password
      MYSQL_ROOT_PASSWORD: rootpassword
    ports:
      - "3306:3306"

  web:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "80:80"
    depends_on:
      - web

volumes:
  mysql_data:
  static_volume:
  media_volume:
```

**Build and Run:**

```bash
# Build images
docker-compose build

# Run migrations
docker-compose run web python manage.py migrate

# Create superuser
docker-compose run web python manage.py createsuperuser

# Start services
docker-compose up -d

# View logs
docker-compose logs -f
```

---

## 🔐 SSL/HTTPS Configuration

### **PythonAnywhere (Automatic)**

PythonAnywhere provides free HTTPS for `.pythonanywhere.com` domains.

For custom domains:
1. Go to **Web** tab
2. Add custom domain
3. Enable HTTPS (Let's Encrypt)

### **Cloudflare (Recommended)**

1. Add domain to Cloudflare
2. SSL/TLS mode: **Full (Strict)**
3. Always Use HTTPS: **On**
4. Automatic HTTPS Rewrites: **On**

---

## 📊 Monitoring & Logging

### **1. Error Logging**

**Sentry Integration:**

```bash
pip install sentry-sdk
```

```python
# settings/production.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)
```

### **2. Application Logs**

```python
# settings/production.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/home/yourusername/logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### **3. Performance Monitoring**

**Django Debug Toolbar (Development Only):**

```python
# settings/development.py
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
```

---

## 🔄 Continuous Deployment

### **GitHub Actions Workflow**

`.github/workflows/deploy.yml`:

```yaml
name: Deploy to PythonAnywhere

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to PythonAnywhere
      env:
        PA_USERNAME: ${{ secrets.PA_USERNAME }}
        PA_API_TOKEN: ${{ secrets.PA_API_TOKEN }}
      run: |
        curl -X POST \
          https://www.pythonanywhere.com/api/v0/user/$PA_USERNAME/webapps/yourdomain.pythonanywhere.com/reload/ \
          -H "Authorization: Token $PA_API_TOKEN"
```

---

## 🗄️ Database Backup & Restore

### **Backup**

```bash
# Manual backup
mysqldump -u username -p olricbookstore_db > backup_$(date +%Y%m%d).sql

# Automated backup (cron job)
0 3 * * * mysqldump -u username -p'password' olricbookstore_db | gzip > ~/backups/db_$(date +\%Y\%m\%d).sql.gz
```

### **Restore**

```bash
mysql -u username -p olricbookstore_db < backup_20260121.sql
```

---

## 🚨 Troubleshooting

### **Issue: 500 Internal Server Error**

**Solution:**
1. Check error logs: `/var/log/yourusername.pythonanywhere.com.error.log`
2. Check WSGI configuration
3. Verify `.env` file exists and is correct
4. Check database connection

### **Issue: Static files not loading**

**Solution:**
1. Run `python manage.py collectstatic`
2. Check static files mapping in Web tab
3. Verify `STATIC_ROOT` in settings
4. Clear browser cache

### **Issue: Database connection error**

**Solution:**
1. Verify database credentials in `.env`
2. Check database exists in Databases tab
3. Test connection: `python manage.py dbshell`

### **Issue: ImportError**

**Solution:**
1. Activate virtual environment
2. Reinstall requirements: `pip install -r requirements.txt`
3. Check Python version compatibility

---

## 📝 Deployment Checklist

### **Before Going Live:**

- [ ] `DEBUG = False` in production settings
- [ ] `ALLOWED_HOSTS` configured
- [ ] `SECRET_KEY` is strong and secret
- [ ] Database backups configured
- [ ] SSL/HTTPS enabled
- [ ] Static files served via CDN
- [ ] Email configuration tested
- [ ] Payment gateway tested (sandbox)
- [ ] Error logging configured (Sentry)
- [ ] Security headers configured
- [ ] CSRF and XSS protection enabled
- [ ] Rate limiting configured
- [ ] Admin panel secured
- [ ] Test all critical user flows
- [ ] Performance testing done
- [ ] SEO meta tags added

### **After Deployment:**

- [ ] Test all pages load correctly
- [ ] Test user registration/login
- [ ] Test cart and checkout
- [ ] Test payment flow (sandbox)
- [ ] Test email notifications
- [ ] Test delivery tracking
- [ ] Monitor error logs
- [ ] Monitor performance
- [ ] Setup uptime monitoring
- [ ] Announce launch! 🎉

---

## 🔗 Useful Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Run tests
python manage.py test

# Check deployment readiness
python manage.py check --deploy

# Database shell
python manage.py dbshell

# Python shell
python manage.py shell

# Clear cache
python manage.py clear_cache

# Update search index
python manage.py update_index
```

---

## 📚 Additional Resources

- [PythonAnywhere Help](https://help.pythonanywhere.com/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [Cloudflare Documentation](https://developers.cloudflare.com/)
- [MilliÖn API Docs](https://millipay.az/docs)

---

**Sənəd versiyası:** 1.0  
**Son yenilənmə:** 2026-01-21  
**Müəllif:** Olric Bookstore Development Team
