from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_index, name='index'),
    path('stats/', views.dashboard_stats, name='stats'),
    path('orders/', views.dashboard_orders, name='orders'),
    path('books/', views.dashboard_books, name='books'),
    path('users/', views.dashboard_users, name='users'),
    path('revenue/', views.dashboard_revenue, name='revenue'),
    path('orders/<int:pk>/', views.dashboard_order_detail, name='order_detail'),
    path('orders/<int:pk>/status/', views.dashboard_update_order_status, name='update_status'),
    path('orders/<int:pk>/assign-courier/', views.dashboard_assign_courier, name='assign_courier'),
    path('couriers/', views.dashboard_couriers, name='couriers'),
    path('couriers/add/', views.dashboard_add_courier, name='add_courier'),
]
