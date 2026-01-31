from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.wishlist_list, name='wishlist_list'),
    path('toggle/<int:book_id>/', views.toggle_wishlist, name='toggle_wishlist'),
]
