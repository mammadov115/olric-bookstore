from django.urls import path
from apps.books.views import HomeView, BookListView, BookDetailView, CategoryBrowseView

app_name = 'books'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('books/', BookListView.as_view(), name='book_list'),
    path('books/<slug:slug>/', BookDetailView.as_view(), name='book_detail'),
    path('categories/', CategoryBrowseView.as_view(), name='category_list'),
    path('category/<slug:category_slug>/', BookListView.as_view(), name='category_books'),
]