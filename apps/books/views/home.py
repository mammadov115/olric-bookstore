from django.views.generic import TemplateView
from apps.books.models import Book, Category
from django.core.cache import cache

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        # Base class-dan mövcud context-i alırıq
        context = super().get_context_data(**kwargs)
        
        # Sənədinə (rules.md) uyğun olaraq aktiv və önə çıxan kitabları gətiririk
        # CACHING: Database query-lərini 15 dəqiqəlik keşləyirik
        
        # 1. Featured Books Cache
        featured_books = cache.get('home_featured_books')
        if not featured_books:
            featured_books = list(Book.objects.with_stats().filter(
                is_active=True, 
                is_featured=True
            ).prefetch_related('authors', 'categories')[:4])
            cache.set('home_featured_books', featured_books, 60 * 15)
        
        context['featured_books'] = featured_books
        
        # 2. Categories Cache
        categories = cache.get('home_categories')
        if not categories:
            categories = list(Category.objects.filter(
                is_active=True, 
                parent=None
            ).order_by('order')[:8])
            cache.set('home_categories', categories, 60 * 15)
            
        context['categories'] = categories
        
        return context
