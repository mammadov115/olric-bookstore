# 🧪 Testing Guide - Olric Bookstore

## 📋 Ümumi Baxış

Bu sənəd Olric Bookstore layihəsinin test strategiyasını, test yazma qaydalarını və best practices-ləri əhatə edir.

---

## 🎯 Testing Strategy

### **Testing Pyramid**

```
        /\
       /  \
      / E2E \           ← End-to-End Tests (Az sayda)
     /______\
    /        \
   /Integration\        ← Integration Tests (Orta sayda)
  /____________\
 /              \
/   Unit Tests   \      ← Unit Tests (Çox sayda)
/__________________\
```

### **Test Coverage Goal**

- **Minimum:** 80% code coverage
- **Target:** 90% code coverage
- **Critical paths:** 100% coverage

---

## 🛠️ Testing Tools

### **1. pytest-django**

```bash
poetry add --group dev pytest pytest-django pytest-cov
```

**pyproject.toml:**
```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.testing"
python_files = ["tests.py", "test_*.py", "*_tests.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--cov=apps",
    "--cov-report=html",
    "--cov-report=term-missing",
    "--verbose",
]
```

### **2. factory_boy**

```bash
poetry add --group dev factory-boy
```

### **3. Faker**

```bash
poetry add --group dev faker
```

### **4. Coverage.py**

Already included with `pytest-cov`.

**Running Tests:**
```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=apps --cov-report=html

# Run specific test file
poetry run pytest tests/test_models.py

# Run specific test
poetry run pytest tests/test_models.py::TestBookModel::test_book_creation
```

---

## 📝 Unit Tests

### **1. Model Tests**

```python
# tests/test_models.py
import pytest
from decimal import Decimal
from apps.books.models import Book, Author, Publisher

@pytest.mark.django_db
class TestBookModel:
    """Test Book model."""
    
    def test_book_creation(self):
        """Test creating a book."""
        publisher = Publisher.objects.create(
            name='Test Publisher',
            slug='test-publisher'
        )
        book = Book.objects.create(
            title='Test Book',
            slug='test-book',
            isbn='1234567890123',
            description='Test description',
            price=Decimal('29.99'),
            stock=10,
            publisher=publisher
        )
        
        assert book.title == 'Test Book'
        assert book.isbn == '1234567890123'
        assert book.price == Decimal('29.99')
        assert str(book) == 'Test Book'
    
    def test_book_final_price_without_discount(self):
        """Test final_price property without discount."""
        book = Book.objects.create(
            title='Test Book',
            slug='test-book',
            isbn='1234567890123',
            description='Test',
            price=Decimal('29.99'),
            stock=10
        )
        
        assert book.final_price == Decimal('29.99')
    
    def test_book_final_price_with_discount(self):
        """Test final_price property with discount."""
        book = Book.objects.create(
            title='Test Book',
            slug='test-book',
            isbn='1234567890123',
            description='Test',
            price=Decimal('29.99'),
            discount_price=Decimal('24.99'),
            stock=10
        )
        
        assert book.final_price == Decimal('24.99')
    
    def test_book_is_in_stock(self):
        """Test is_in_stock method."""
        book = Book.objects.create(
            title='Test Book',
            slug='test-book',
            isbn='1234567890123',
            description='Test',
            price=Decimal('29.99'),
            stock=0
        )
        
        assert book.is_in_stock() is False
        
        book.stock = 5
        book.save()
        
        assert book.is_in_stock() is True
    
    def test_book_unique_isbn(self):
        """Test ISBN uniqueness constraint."""
        Book.objects.create(
            title='Book 1',
            slug='book-1',
            isbn='1234567890123',
            description='Test',
            price=Decimal('29.99'),
            stock=10
        )
        
        with pytest.raises(Exception):  # IntegrityError
            Book.objects.create(
                title='Book 2',
                slug='book-2',
                isbn='1234567890123',  # Duplicate ISBN
                description='Test',
                price=Decimal('29.99'),
                stock=10
            )
```

---

### **2. View Tests**

```python
# tests/test_views.py
import pytest
from django.urls import reverse
from apps.books.models import Book

@pytest.mark.django_db
class TestBookViews:
    """Test Book views."""
    
    def test_book_list_view(self, client):
        """Test book list view."""
        # Create test books
        Book.objects.create(
            title='Book 1',
            slug='book-1',
            isbn='1111111111111',
            description='Test',
            price='29.99',
            stock=10
        )
        Book.objects.create(
            title='Book 2',
            slug='book-2',
            isbn='2222222222222',
            description='Test',
            price='39.99',
            stock=5
        )
        
        # Get book list page
        url = reverse('books:list')
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'Book 1' in response.content.decode()
        assert 'Book 2' in response.content.decode()
    
    def test_book_detail_view(self, client):
        """Test book detail view."""
        book = Book.objects.create(
            title='Test Book',
            slug='test-book',
            isbn='1234567890123',
            description='Test description',
            price='29.99',
            stock=10
        )
        
        url = reverse('books:detail', kwargs={'slug': book.slug})
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'Test Book' in response.content.decode()
        assert 'Test description' in response.content.decode()
    
    def test_book_detail_view_404(self, client):
        """Test book detail view with non-existent book."""
        url = reverse('books:detail', kwargs={'slug': 'non-existent'})
        response = client.get(url)
        
        assert response.status_code == 404
    
    def test_book_search_view(self, client):
        """Test book search functionality."""
        Book.objects.create(
            title='The Great Gatsby',
            slug='the-great-gatsby',
            isbn='1111111111111',
            description='Classic novel',
            price='29.99',
            stock=10
        )
        Book.objects.create(
            title='To Kill a Mockingbird',
            slug='to-kill-a-mockingbird',
            isbn='2222222222222',
            description='Another classic',
            price='24.99',
            stock=5
        )
        
        url = reverse('books:search')
        response = client.get(url, {'q': 'gatsby'})
        
        assert response.status_code == 200
        assert 'The Great Gatsby' in response.content.decode()
        assert 'To Kill a Mockingbird' not in response.content.decode()
```

---

### **3. Form Tests**

```python
# tests/test_forms.py
import pytest
from apps.reviews.forms import ReviewForm

class TestReviewForm:
    """Test Review form."""
    
    def test_review_form_valid(self):
        """Test valid review form."""
        form_data = {
            'rating': 5,
            'title': 'Great book!',
            'content': 'This is a great book. I highly recommend it to everyone.'
        }
        form = ReviewForm(data=form_data)
        
        assert form.is_valid()
    
    def test_review_form_invalid_rating(self):
        """Test invalid rating."""
        form_data = {
            'rating': 6,  # Invalid (max is 5)
            'title': 'Great book!',
            'content': 'This is a great book.'
        }
        form = ReviewForm(data=form_data)
        
        assert not form.is_valid()
        assert 'rating' in form.errors
    
    def test_review_form_short_content(self):
        """Test content too short."""
        form_data = {
            'rating': 5,
            'title': 'Great!',
            'content': 'Good'  # Too short (min 20 chars)
        }
        form = ReviewForm(data=form_data)
        
        assert not form.is_valid()
        assert 'content' in form.errors
```

---

## 🔗 Integration Tests

### **1. Cart & Checkout Flow**

```python
# tests/test_integration.py
import pytest
from decimal import Decimal
from django.urls import reverse
from apps.books.models import Book
from apps.cart.models import Cart, CartItem
from apps.orders.models import Order

@pytest.mark.django_db
class TestCheckoutFlow:
    """Test complete checkout flow."""
    
    def test_add_to_cart_and_checkout(self, client, django_user_model):
        """Test adding to cart and completing checkout."""
        # Create user
        user = django_user_model.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create book
        book = Book.objects.create(
            title='Test Book',
            slug='test-book',
            isbn='1234567890123',
            description='Test',
            price=Decimal('29.99'),
            stock=10
        )
        
        # Login
        client.login(username='testuser', password='testpass123')
        
        # Add to cart
        url = reverse('cart:add')
        response = client.post(url, {'book_id': book.id})
        assert response.status_code == 200
        
        # Check cart
        cart = Cart.objects.get(user=user)
        assert cart.items.count() == 1
        assert cart.items.first().book == book
        
        # Checkout
        checkout_url = reverse('orders:checkout')
        checkout_data = {
            'billing_name': 'Test User',
            'billing_email': 'test@example.com',
            'billing_phone': '+994501234567',
            'billing_address': 'Test Address',
            'billing_city': 'Baku',
            'shipping_name': 'Test User',
            'shipping_phone': '+994501234567',
            'shipping_address': 'Test Address',
            'shipping_city': 'Baku',
            'payment_method': 'cash'
        }
        response = client.post(checkout_url, checkout_data)
        
        # Check order created
        assert Order.objects.filter(user=user).exists()
        order = Order.objects.get(user=user)
        assert order.items.count() == 1
        assert order.total == Decimal('29.99')
```

---

### **2. Payment Integration**

```python
# tests/test_payment.py
import pytest
from decimal import Decimal
from unittest.mock import patch, Mock
from apps.payments.services import MilliPayService
from apps.orders.models import Order

@pytest.mark.django_db
class TestPaymentIntegration:
    """Test payment integration."""
    
    @patch('apps.payments.services.requests.post')
    def test_create_payment(self, mock_post, django_user_model):
        """Test creating payment with MilliÖn."""
        # Mock MilliÖn API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': 'success',
            'payment_url': 'https://millipay.az/payment/abc123',
            'transaction_id': 'TXN-123'
        }
        mock_post.return_value = mock_response
        
        # Create order
        user = django_user_model.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        order = Order.objects.create(
            order_number='ORD-001',
            user=user,
            billing_name='Test User',
            billing_email='test@example.com',
            billing_phone='+994501234567',
            billing_address='Test Address',
            billing_city='Baku',
            shipping_name='Test User',
            shipping_phone='+994501234567',
            shipping_address='Test Address',
            shipping_city='Baku',
            subtotal=Decimal('29.99'),
            total=Decimal('29.99'),
            payment_method='online'
        )
        
        # Create payment
        service = MilliPayService()
        result = service.create_payment(order)
        
        assert result['status'] == 'success'
        assert 'payment_url' in result
        assert 'transaction_id' in result
```

---

## 🏭 Factory Pattern

### **Using factory_boy**

```python
# tests/factories.py
import factory
from factory.django import DjangoModelFactory
from faker import Faker
from apps.books.models import Book, Author, Publisher
from apps.accounts.models import User

fake = Faker()

class UserFactory(DjangoModelFactory):
    """User factory."""
    
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    role = 'customer'

class PublisherFactory(DjangoModelFactory):
    """Publisher factory."""
    
    class Meta:
        model = Publisher
    
    name = factory.Faker('company')
    slug = factory.Sequence(lambda n: f'publisher-{n}')

class AuthorFactory(DjangoModelFactory):
    """Author factory."""
    
    class Meta:
        model = Author
    
    name = factory.Faker('name')
    slug = factory.Sequence(lambda n: f'author-{n}')
    bio = factory.Faker('text')

class BookFactory(DjangoModelFactory):
    """Book factory."""
    
    class Meta:
        model = Book
    
    title = factory.Faker('sentence', nb_words=4)
    slug = factory.Sequence(lambda n: f'book-{n}')
    isbn = factory.Sequence(lambda n: f'{n:013d}')
    description = factory.Faker('text')
    price = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True)
    stock = factory.Faker('random_int', min=0, max=100)
    publisher = factory.SubFactory(PublisherFactory)
    
    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for author in extracted:
                self.authors.add(author)
        else:
            self.authors.add(AuthorFactory())
```

**Using Factories in Tests:**

```python
# tests/test_with_factories.py
import pytest
from tests.factories import BookFactory, UserFactory, AuthorFactory

@pytest.mark.django_db
class TestWithFactories:
    """Test using factories."""
    
    def test_create_book_with_factory(self):
        """Test creating book with factory."""
        book = BookFactory()
        
        assert book.title is not None
        assert book.isbn is not None
        assert book.price > 0
        assert book.authors.count() == 1
    
    def test_create_multiple_books(self):
        """Test creating multiple books."""
        books = BookFactory.create_batch(10)
        
        assert len(books) == 10
    
    def test_create_book_with_specific_author(self):
        """Test creating book with specific author."""
        author = AuthorFactory(name='F. Scott Fitzgerald')
        book = BookFactory(authors=[author])
        
        assert book.authors.first().name == 'F. Scott Fitzgerald'
```

---

## 📊 Test Coverage

### **Running Coverage**

```bash
# Run tests with coverage
pytest --cov=apps --cov-report=html --cov-report=term-missing

# View HTML report
open htmlcov/index.html
```

### **Coverage Configuration**

**.coveragerc:**
```ini
[run]
source = apps
omit = 
    */migrations/*
    */tests/*
    */admin.py
    */apps.py
    */__init__.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
```

---

## 🎭 Mocking & Patching

### **Mocking External APIs**

```python
# tests/test_google_books_api.py
import pytest
from unittest.mock import patch, Mock
from apps.books.services import GoogleBooksService

class TestGoogleBooksAPI:
    """Test Google Books API integration."""
    
    @patch('apps.books.services.requests.get')
    def test_fetch_book_by_isbn(self, mock_get):
        """Test fetching book data from Google Books API."""
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'items': [{
                'volumeInfo': {
                    'title': 'The Great Gatsby',
                    'authors': ['F. Scott Fitzgerald'],
                    'description': 'Classic novel...',
                    'publishedDate': '2004-09-30',
                    'pageCount': 180
                }
            }]
        }
        mock_get.return_value = mock_response
        
        # Test service
        service = GoogleBooksService()
        result = service.fetch_by_isbn('9780743273565')
        
        assert result['title'] == 'The Great Gatsby'
        assert 'F. Scott Fitzgerald' in result['authors']
```

---

## 🔄 Fixtures

### **pytest Fixtures**

```python
# conftest.py
import pytest
from apps.books.models import Book
from apps.accounts.models import User

@pytest.fixture
def user(django_user_model):
    """Create test user."""
    return django_user_model.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )

@pytest.fixture
def admin_user(django_user_model):
    """Create admin user."""
    return django_user_model.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )

@pytest.fixture
def book():
    """Create test book."""
    return Book.objects.create(
        title='Test Book',
        slug='test-book',
        isbn='1234567890123',
        description='Test description',
        price='29.99',
        stock=10
    )

@pytest.fixture
def authenticated_client(client, user):
    """Return authenticated client."""
    client.login(username='testuser', password='testpass123')
    return client
```

**Using Fixtures:**

```python
@pytest.mark.django_db
def test_with_fixtures(authenticated_client, book):
    """Test using fixtures."""
    url = reverse('cart:add')
    response = authenticated_client.post(url, {'book_id': book.id})
    
    assert response.status_code == 200
```

---

## 🚀 Performance Tests

### **Load Testing with Locust**

```bash
poetry add --group dev locust
```

**locustfile.py:**

```python
from locust import HttpUser, task, between

class BookstoreUser(HttpUser):
    """Simulate bookstore user."""
    
    wait_time = between(1, 3)
    
    @task(3)
    def browse_books(self):
        """Browse book list."""
        self.client.get('/books/')
    
    @task(2)
    def view_book_detail(self):
        """View book detail."""
        self.client.get('/books/test-book/')
    
    @task(1)
    def search_books(self):
        """Search books."""
        self.client.get('/books/search/?q=gatsby')
    
    def on_start(self):
        """Login on start."""
        self.client.post('/accounts/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
```

**Run Load Test:**

```bash
locust -f locustfile.py --host=http://localhost:8000
# Open http://localhost:8089
```

---

## 📝 Test Organization

### **Directory Structure**

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── factories.py             # Factory Boy factories
├── unit/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   ├── test_forms.py
│   └── test_utils.py
├── integration/
│   ├── __init__.py
│   ├── test_checkout_flow.py
│   ├── test_payment.py
│   └── test_delivery.py
└── performance/
    ├── __init__.py
    └── locustfile.py
```

---

## ✅ Testing Best Practices

### **1. Test Naming**

```python
# ✅ DÜZGÜN - Descriptive names
def test_book_creation_with_valid_data():
    pass

def test_book_creation_fails_with_duplicate_isbn():
    pass

# ❌ YANLIŞ - Unclear names
def test_book1():
    pass

def test_book2():
    pass
```

### **2. AAA Pattern (Arrange-Act-Assert)**

```python
def test_add_to_cart():
    # Arrange
    user = User.objects.create_user(username='test', password='test')
    book = Book.objects.create(title='Test', isbn='123', price='29.99')
    
    # Act
    cart = Cart.objects.create(user=user)
    cart_item = CartItem.objects.create(cart=cart, book=book, quantity=1)
    
    # Assert
    assert cart.items.count() == 1
    assert cart_item.book == book
```

### **3. One Assertion Per Test (Flexible)**

```python
# ✅ Focused test
def test_book_title():
    book = Book.objects.create(title='Test', isbn='123', price='29.99')
    assert book.title == 'Test'

# ✅ Related assertions OK
def test_book_creation():
    book = Book.objects.create(title='Test', isbn='123', price='29.99')
    assert book.title == 'Test'
    assert book.isbn == '123'
    assert str(book) == 'Test'
```

### **4. Test Independence**

```python
# ✅ DÜZGÜN - Independent tests
@pytest.mark.django_db
def test_create_book():
    book = Book.objects.create(title='Test', isbn='123', price='29.99')
    assert Book.objects.count() == 1

@pytest.mark.django_db
def test_delete_book():
    book = Book.objects.create(title='Test', isbn='123', price='29.99')
    book.delete()
    assert Book.objects.count() == 0

# ❌ YANLIŞ - Tests depend on each other
def test_create_then_delete():
    # Don't do this!
    pass
```

---

## 🎯 CI/CD Integration

### **GitHub Actions**

**.github/workflows/tests.yml:**

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_DATABASE: test_db
          MYSQL_ROOT_PASSWORD: password
        ports:
          - 3306:3306
        options: --health-cmd="mysqladmin ping" --health-interval=10s --health-timeout=5s --health-retries=3
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.10
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests
      env:
        DB_HOST: 127.0.0.1
        DB_PORT: 3306
        DB_NAME: test_db
        DB_USER: root
        DB_PASSWORD: password
      run: |
        pytest --cov=apps --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
      with:
        file: ./coverage.xml
```

---

## 📋 Pre-Commit Testing

### **pre-commit hook**

**.git/hooks/pre-commit:**

```bash
#!/bin/bash

# Run tests before commit
pytest tests/unit/ -v

if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi

echo "All tests passed!"
```

---

## 🎓 Testing Checklist

### **Before Committing:**
- [ ] All tests passing
- [ ] New features have tests
- [ ] Bug fixes have regression tests
- [ ] Code coverage >= 80%
- [ ] No skipped tests without reason

### **Test Types:**
- [ ] Unit tests (models, views, forms, utils)
- [ ] Integration tests (user flows)
- [ ] API tests (if applicable)
- [ ] Performance tests (critical paths)

### **Test Quality:**
- [ ] Descriptive test names
- [ ] AAA pattern followed
- [ ] Tests are independent
- [ ] Fixtures used appropriately
- [ ] Mocking external services

---

**Sənəd versiyası:** 1.0  
**Son yenilənmə:** 2026-01-21  
**Müəllif:** Olric Bookstore Development Team
