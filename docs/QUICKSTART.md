# 🚀 Quick Start Guide - Olric Bookstore

## 📋 Prerequisites

- Python 3.10+
- Poetry (package manager)
- MySQL 8.0+
- Git

---

## 🔧 Installation

### **1. Install Poetry**

**Windows (PowerShell):**
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

**Linux/macOS:**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

**Verify Installation:**
```bash
poetry --version
```

---

### **2. Clone Repository**

```bash
git clone https://github.com/yourusername/olric-bookstore.git
cd olric-bookstore
```

---

### **3. Install Dependencies**

```bash
# Install all dependencies (including dev)
poetry install

# Or install without dev dependencies
poetry install --without dev
```

---

### **4. Setup Environment Variables**

Create `.env` file in project root:

```bash
# Copy example env file
cp .env.example .env
```

Edit `.env` file:

```env
# Django Settings
SECRET_KEY=your-super-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=olric_bookstore
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306

# Email (for development)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# MilliÖn Payment (test mode)
MILLIPAY_MERCHANT_ID=test-merchant-id
MILLIPAY_SECRET_KEY=test-secret-key
MILLIPAY_TEST_MODE=True
```

---

### **5. Setup Database**

**Create MySQL Database:**

```sql
CREATE DATABASE olric_bookstore CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**Run Migrations:**

```bash
poetry run python manage.py migrate
```

---

### **6. Create Superuser**

```bash
poetry run python manage.py createsuperuser
```

---

### **7. Load Initial Data (Optional)**

```bash
# Load categories, publishers, etc.
poetry run python manage.py loaddata initial_data.json

# Or generate fake data for testing
poetry run python manage.py seed_data
```

---

### **8. Setup Tailwind CSS (CDN)**

Tailwind CSS CDN istifadə edəcəyik - no build step lazım deyil!

Create `templates/base.html`:

```html
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Olric Bookstore{% endblock %}</title>
    
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Tailwind Custom Config -->
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
    
    <!-- Font Awesome CDN -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    
    <!-- Custom CSS (optional) -->
    <link rel="stylesheet" href="{% static 'css/custom.css' %}">
</head>
<body class="bg-gray-50">
    {% block content %}{% endblock %}
    
    <!-- jQuery CDN -->
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    
    <!-- Custom JS -->
    {% block extra_js %}{% endblock %}
</body>
</html>
```

**Üstünlüklər:**
- ✅ No Node.js required
- ✅ No build step
- ✅ Instant development
- ✅ Easy deployment

---

### **9. Run Development Server**

```bash
# Activate Poetry shell
poetry shell

# Run server
python manage.py runserver

# Or run without activating shell
poetry run python manage.py runserver
```

Visit: `http://localhost:8000`

---

## 🧪 Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=apps --cov-report=html

# Run specific test file
poetry run pytest tests/test_models.py

# Open coverage report
open htmlcov/index.html
```

---

## 🎨 Code Formatting

```bash
# Format code with Black
poetry run black .

# Sort imports with isort
poetry run isort .

# Lint with flake8
poetry run flake8 .

# Run all formatters
poetry run black . && poetry run isort . && poetry run flake8 .
```

---

## 📦 Useful Poetry Commands

```bash
# Add new dependency
poetry add package-name

# Add dev dependency
poetry add --group dev package-name

# Remove dependency
poetry remove package-name

# Update dependencies
poetry update

# Show installed packages
poetry show

# Show outdated packages
poetry show --outdated

# Export requirements.txt (if needed)
poetry export -f requirements.txt --output requirements.txt
```

---

## 🐳 Docker (Optional)

```bash
# Build and run with Docker Compose
docker-compose up -d

# Run migrations in Docker
docker-compose exec web poetry run python manage.py migrate

# Create superuser in Docker
docker-compose exec web poetry run python manage.py createsuperuser

# View logs
docker-compose logs -f
```

---

## 📚 Project Structure

```
olric-bookstore/
├── apps/                    # Django applications
│   ├── accounts/           # User management
│   ├── books/              # Book catalog
│   ├── cart/               # Shopping cart
│   ├── orders/             # Order management
│   └── ...
├── config/                 # Project configuration
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User uploads
├── tests/                  # Test files
├── docs/                   # Documentation
├── pyproject.toml          # Poetry configuration
├── .env                    # Environment variables
├── .gitignore
├── manage.py
└── README.md
```

---

## 🔗 Useful Links

- **Documentation:** `docs/`
- **Tech Stack:** `docs/tech-stack.md`
- **Architecture:** `docs/architect.md`
- **Coding Rules:** `docs/rules.md`
- **Deployment Guide:** `docs/deployment-guide.md`
- **Security Checklist:** `docs/security-checklist.md`
- **Testing Guide:** `docs/testing-guide.md`

---

## 🆘 Troubleshooting

### **Poetry not found**
```bash
# Add Poetry to PATH
export PATH="$HOME/.local/bin:$PATH"
```

### **MySQL connection error**
- Check MySQL is running
- Verify database credentials in `.env`
- Ensure database exists

### **Static files not loading**
```bash
poetry run python manage.py collectstatic
```

---

## 📞 Support

For issues and questions:
- Check documentation in `docs/`
- Review `README.md`
- Contact: team@olricbookstore.com

---

**Happy Coding! 🚀**
