# 📚 Olric Bookstore - Project Implementation Roadmap

Bu sənəd layihənin inkişaf mərhələlərini izləmək üçün nəzərdə tutulub.
**Status:** 🟢 - Tamamlanıb | 🟡 - Davam edir | ⚪ - Gözləyir

---

## 🏗️ Mərhələ 1: İnfrastruktur və Konfiqurasiya
- [x] Poetry mühitinin qurulması və asılılıqların quraşdırılması (Django, Pillow, etc.)
- [x] Proyekt strukturunun yaradılması (`apps/`, `config/settings/`)
- [x] Environment variables tənzimləmələri (`.env` və `django-environ`)
- [x] Multi-settings konfiqurasiyası (`base.py`, `development.py`)
- [x] SQLite development bazasının sazlanması və Cache xətalarının həlli

## 👤 Mərhələ 2: User Management (Accounts App)
- [x] Custom User modelinin yaradılması (Email identifier, Role-based)
- [x] Custom UserManager (create_user, create_superuser) yaradılması
- [x] Auth sistemindəki `related_name` toqquşmalarının həlli
- [x] User Profile modeli və preferences (JSON field)
- [x] Login/Register API və ya View-ların yazılması (JWT və ya Session)

## 📖 Mərhələ 3: Kitab Kataloqu (Books App)
- [x] `Author` və `Publisher` modellərinin yaradılması
- [x] `Category` modeli (Self-referencing parent-child structure)
- [x] `Book` modeli (ISBN, Slug, Price, Stock, Many-to-Many with Authors/Categories)
- [x] Book detail, list və filter (category, price, author) məntiqləri
- [x] Search funksionallığı (Full-text search)

## 🛒 Mərhələ 4: Shopping Cart & Orders
- [ ] `Cart` və `CartItem` modelləri (Session-based və ya User-based)
- [ ] `Order` və `OrderItem` modelləri (Order numbering logic)
- [ ] Sifariş prosesi (Checkout workflow)
- [ ] `Coupon` sistemi (Discount percentage/fixed, usage limits)

## 💳 Mərhələ 5: Ödəniş və Çatdırılma
- [ ] MilliPAY inteqrasiyası (`Payment` modeli və callback handle)
- [ ] `Courier` və `Delivery` modelləri
- [ ] Tracking sistemi (Tracking number generation)
- [ ] Delivery Status Update logikası

## 🌟 Mərhələ 6: Müştəri Təcrübəsi (Reviews & Wishlist)
- [ ] `Review` sistemi (Rating 1-5, Verified purchase check)
- [ ] `Wishlist` funksionallığı
- [ ] Email/SMS Notification sistemi (Template-based)

## 🎨 Mərhələ 7: Frontend & UI (Tailwind CSS)
- [ ] Base template və layout-ların hazırlanması
- [ ] Navbar, Footer və Responsive dizayn
- [ ] Kitab kartları və slider-lər
- [ ] İstifadəçi paneli (Dashboard)

## 🚀 Mərhələ 8: Production & Deployment
- [ ] PostgreSQL keçidi (Production settings)
- [ ] Gunicorn/Nginx konfiqurasiyası
- [ ] Dockerization (Optional)
- [ ] SSL və Təhlükəsizlik tənzimləmələri (Security Check)

---

## 📝 Cari Vəziyyət (AI üçün qeyd)
- **Son görülən iş:** `accounts.User` modeli və `development.py` bazası tam hazırdır. 
- **Növbəti addım:** `books` app-i daxilində modelləri (Category, Author, Book) tamamlamaq və ilk migration-ı icra etmək.