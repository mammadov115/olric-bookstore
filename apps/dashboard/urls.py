from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_index, name='index'),
    path('stats/', views.dashboard_stats, name='stats'),
    path('orders/', views.dashboard_orders, name='orders'),
    path('books/', views.dashboard_books, name='books'),
    path('users/', views.dashboard_users, name='users'),
]
