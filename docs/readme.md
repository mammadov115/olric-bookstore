Project Bookstore projecti olacaq.
Aşağıdakı təlimatlara uyğun olaraq tech-stack.md, architect.md, rules.md fayllarını hazırlamalısan. Sonra isə mən hazırladığın bu 3 faylı review edəcəm. Bəyəndikdən sonra isə bunları tətbiq edərsən:
1. Layihənin adı: Olric Bookstore
2. Layihənin məqsədi: Onlayn kitab satışını tətbiq etməkdir.
3. Layihənin texniki tələbləri: 
    - Lahiyənin dizaynı https://www.penguin.co.uk/ saytından ilhamlanaraq hazırlanacaq. Rənglər, fontlar, layoutlar, elementlər, animasiyalar, bütün dizayn elementləri eyni olacaq. Hətta eyni elementlər eyni yerlərdə olacaq. Yəni dizayn baxımından tam olaraq eyni olacaq.
    - Lahiyənin texniki tələbləri: 
        - Lahiyə Django ilə hazırlanacaq.
        - Monolith strukturda olacaq
        - Package Manager: Poetry (modern dependency management)
        - Frontend: Tailwind CSS (CDN - no build step)
        - Fonts: Font Awesome
        - Database: Mysql(Hələlik bu olacaq, sonra isə lazım olarsa PostgreSQL olacaq)
        - ORM: Django ORM
        - Authentication: Django Authentication
        - Payment: 
            - Xarici bazar üçün: Olmayacaq (hələlik)
            - Azərbaycan bazarı üçün: MilliÖn (Payment Aggregator)
            - Nağd ödəniş (Cash on Delivery)
        - Deployment: Pythonanywhere(Hələlik, sonra isə lazım olarsa başqa bir platforma olacaq)
        - Docker: Gələcək deployment və development üçün containerization hazırlanacaq (Docker + Docker Compose)
        - Environment Variables: .env faylı ilə konfiqurasiya (SECRET_KEY, DATABASE, EMAIL, PAYMENT_KEYS və s.)
        - Static Files & CDN: Cloudflare CDN (pulsuz plan) istifadə ediləcək
        - JS: Jquery istifadə olunacaq (separated files, HTML-dən ayrı)
        - API: REST API (lazım olarsa - Django REST Framework)
3. Layihənin funksional tələbləri:
    - Delivery tracking sistemi olacaq:
        - Real-time GPS tracking 
        - Status updates (Sifariş verildi, Hazırlanır, Yoldadır, Çatdırıldı)
        - SMS və Email bildirişləri
    - Online ödəniş sistemi olacaq (Lokal banklar, Nağd ödəniş).
    - Kitab məlumatları:
        - Manual entry (Admin panel vasitəsilə)
        - External API integration (Google Books API və ya digər kitab API-ləri)
    - Wishlist/Favorites funksiyası - İstifadəçilər bəyəndikləri kitabları yadda saxlaya biləcəklər.
    - Book reviews və ratings sistemi - Müştərilər kitablar haqqında rəy yaza və reytinq verə biləcəklər.
    - Search və filtering sistemi - Müəllif, janr, qiymət aralığı, nəşriyyat, dil və s. əsasında axtarış.
    - Email notifications - Sifariş təsdiqi, göndəriş statusu, kampaniyalar haqqında bildirişlər.
    - Kupon/Discount code sistemi - Endirim kuponları və promo kodlar.
    - Custom adminpanel olacaq:
        - Djangonun default adminpanelindən istifadə olunmayacaq
        - Django templates + Tailwind CSS ilə hazırlanacaq
        - Responsive və modern dizayn
    - Adminpaneldə aşağıdakı funksionallıqlar olacaq:
        - Stok idarəetmə
        - Sifariş idarəetmə
        - Müştəri idarəetmə
        - Ödəniş idarəetmə
        - Kuryer idarəetmə
        - Kupon/Endirim idarəetmə
        - Rəy və reytinq moderasiyası
        - Kitab məlumatları idarəetmə (CRUD operations)
        - Dashboard və statistika
4. İlkin olaraq 2 dildə olacaq: Azərbaycan və İngilis dili. Sonra isə lazım olarsa başqa dillər əlavə oluna bilər.
5. İlkin olaraq 3 fərqli rol olacaq: Admin, Kuryer, Müştəri. Sonra isə lazım olarsa başqa rollar əlavə oluna bilər.
6. İlkin olaraq fake datalar yüklə ki, layihənin dizaynı və funksionallığı test edilə bilsin.
7. Təhlükəsizlik tələbləri:
    - CSRF Protection: Django default olaraq təmin edir, amma bütün formlarda yoxlanılmalıdır
    - XSS Protection: User input-ları sanitize edilməlidir, Django templates auto-escape istifadə edir
    - Rate Limiting: Brute force hücumlarına qarşı (django-ratelimit və ya django-axes istifadə ediləcək)
    - SSL/HTTPS: PythonAnywhere dəstəkləyir, production-da mütləq aktiv olmalıdır
    - Payment Data Security: PCI DSS compliance, ödəniş məlumatları heç vaxt database-də saxlanılmamalıdır
    - SQL Injection Protection: Django ORM istifadə ediləcək (raw queries minimuma endirilməlidir)
    - Password Security: Django-nun default password hashers (PBKDF2) istifadə ediləcək
    - Session Security: Secure cookies, HTTPS-only sessions
8. Testing strategiyası:
    - Unit Tests: Django TestCase istifadə ediləcək (models, views, forms, utilities)
    - Integration Tests: Ödəniş prosesi, delivery tracking, email notifications
    - Fake Data Generation: Faker library istifadə ediləcək (development və testing üçün)
    - Coverage: Minimum 80% code coverage hədəfi
    - Testing Tools: pytest-django, coverage.py, factory_boy
9. Hazırlanmalı olan əlavə sənədlər:
    - tech-stack.md - Texnologiyalar və seçim səbəbləri
    - architect.md - Sistem arxitekturası, models, apps strukturu, database schema
    - rules.md - Kodlaşdırma standartları, naming conventions, best practices
    - database-schema.md - Verilənlər bazası strukturu (ER diagram, table relationships)
    - api-endpoints.md - API documentation (lazım olarsa - REST endpoints)
    - deployment-guide.md - Deployment addımları (PythonAnywhere, Docker, environment setup)
    - security-checklist.md - Təhlükəsizlik yoxlama siyahısı
    - testing-guide.md - Test yazma qaydaları və nümunələr
