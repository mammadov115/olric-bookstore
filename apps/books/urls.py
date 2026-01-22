from django.urls import path
from apps.books.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]