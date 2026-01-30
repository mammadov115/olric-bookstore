# 📚 Olric Bookstore - Implementation Roadmap

This document serves as the primary tracking mechanism for the development of Olric Bookstore.

**Status Legend:**
- 🟢 **Completed**
- 🟡 **In Progress**
- ⚪ **Pending**

---

## 🏗️ 1. Infrastructure & Core Foundation
*Establishing the bedrock for a scalable and maintainable Django application.*

- [x] **Development Environment Setup**
    - **Action:** Initialize project with Poetry, configure Django, and install core dependencies.
    - **Visual/Functional Result:** Working project directory with isolated virtual environment and standard folder structure.
- [x] **Advanced Settings Architecture**
    - **Action:** Implement a multi-stage settings system (`base.py`, `development.py`, `production.py`) using `django-environ`.
    - **Visual/Functional Result:** Environment-specific behavior (e.g., SQLite for dev, PostgreSQL for prod) controlled via `.env` file.
- [x] **Modular App Structure**
    - **Action:** Configure `apps/` as a secondary source directory for cleaner project organization.
    - **Visual/Functional Result:** Scalable codebase where feature-specific apps are neatly grouped.

## 👤 2. Identity & Access Management (Accounts App)
*User authentication, authorization, and personalized profiles.*

- [x] **Custom User Engine**
    - **Model:** `User` (Email as primary identifier, Role-based fields).
    - **Logic:** Custom `UserManager` to handle email-based authentication.
    - **Visual/Functional Result:** Users login with email instead of username; Role-based separation (Admin, Customer, Courier).
- [x] **Persona & Profile System**
    - **Model:** `Profile` with JSON-based `preferences` and `social_links`.
    - **Logic:** Automated profile creation via Django `post_save` signals.
    - **Visual/Functional Result:** Every new user automatically gets a customizable profile for theme/notification settings.
- [x] **Authentication Suite**
    - **Views:** Login, Registration, Logout.
    - **Templates:** Tailwind CSS styled authentication pages.
    - **Visual/Functional Result:** Mobile-responsive, professional-looking entry points for users.

## 📖 3. Digital Catalog (Books App)
*The core of the bookstore - managing and navigating book data.*

- [x] **Structural Taxonomy**
    - **Models:** `Category` (Hierarchical/Tree structure), `Author`, `Publisher`.
    - **Visual/Functional Result:** Administrative capability to nested genres (e.g., Fiction > Mystery > Noir) and link authors/publishers.
- [x] **Master Book Index**
    - **Model:** `Book` (ISBN-13, Slug, Prices, Stock, Multi-Category/Author support).
    - **Visual/Functional Result:** Comprehensive data coverage including pagination, format (Hardcover/E-book), and metadata.
- [x] **Discovery Interface**
    - **Views:** Book List, Book Detail, Category Browse.
    - **Templates:** Product grids and feature-rich detail pages.
    - **Visual/Functional Result:** Users can browse the collection, view high-res book covers, and read descriptions in a clean UI.
- [x] **Search & Filtering Intelligence**
    - **Logic:** Full-text search and faceted filtering (by author, price range, format).
    - **Visual/Functional Result:** A search bar that delivers instant results and sidebar filters to narrow down the catalog.

## 🛒 4. Commerce & Shopping Flow (Cart App)
*Facilitating a smooth selection process for shoppers.*

- [x] **Universal Shopping Cart**
    - **Models:** `Cart`, `CartItem`.
    - **Logic:** Session-based persistence for guests and DB-sync for registered users.
    - **Visual/Functional Result:** A persistent cart that remembers items across sessions with AJAX-based quantity updates.
- [x] **Dynamic Cart UI**
    - **Template:** Floating cart summary and a dedicated Cart management page.
    - **Visual/Functional Result:** Real-time feedback when adding books to cart without page refreshes.

## 💳 5. Orders & Financial Fulfillment (Orders & Payments)
*Recording transactions and processing secure payments.*

- [x] **Order Management Engine**
    - **Models:** `Order`, `OrderItem` (capturing price snapshots at time of purchase).
    - **Visual/Functional Result:** Permanent order history for users and an administration dashboard for fulfillment.
- [x] **MilliPAY Integration**
    - **Logic:** Secure payment gateway integration for local bank cards.
    - **Visual/Functional Result:** Customers are redirected to the secure portal and return to a "Success" page upon completion.
- [x] **Promotional System (Coupons)**
    - **Model:** `Coupon` (Percentage or Fixed discounts, usage limits).
    - **Visual/Functional Result:** A "Voucher Code" field during checkout that instantly recalculates the total.

## 🚚 6. Logistics & Delivery (Delivery App)
*Tracking the physical journey of the books.*

- [ ] **Fulfillment Tracking**
    - **Models:** `Courier`, `Delivery`.
    - **Visual/Functional Result:** Internal tracking system for staff to assign couriers and update delivery status.
- [ ] **Customer Tracking Dashboard**
    - **Logic:** Unique tracking numbers and progress visualization.
    - **Visual/Functional Result:** A tracking page where customers see the real-time status (Picked up > En route > Delivered).

## 🌟 7. Engagement & Social Proof (Reviews & Wishlist)
*Building community trust and user retention.*

- [ ] **Rating & Feedback Suite**
    - **Model:** `Review` (1-5 Stars, Verified Purchase badge).
    - **Visual/Functional Result:** Star ratings displayed on book cards and user reviews section on detail pages.
- [ ] **Personal Wishlist**
    - **Model:** `Wishlist`.
    - **Visual/Functional Result:** A "Heart" icon on books allowing users to save items for future purchase.

## 📢 8. Automated Communication (Notifications)
*Engagement through Email and SMS.*

- [ ] **Transaction Alerts**
    - **Logic:** Trigger-based notifications for order status changes.
    - **Visual/Functional Result:** Automated emails sent to users upon successful payment and delivery dispatch.

## 📊 9. Admin Intelligence (Dashboard App)
*Command and control for store operators.*

- [ ] **Store Operations Center**
    - **Views:** Custom dashboard with sales analytics, inventory alerts, and user reports.
    - **Visual/Functional Result:** A visually rich management interface with charts (Chart.js) showing revenue trends.

---

## � 10. Production Deployment
*Optimizing and launching the bookstore.*

- [ ] **Production Readiness**
    - **Tasks:** PostgreSQL migration, Gunicorn/Nginx configuration, Security headers.
    - **Visual/Functional Result:** A lightning-fast Bookstore accessible via a secure HTTPS domain.