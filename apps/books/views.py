from django.views.generic import TemplateView
from apps.books.models import Book, Category

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        # Base class-dan mövcud context-i alırıq
        context = super().get_context_data(**kwargs)
        
        # Sənədinə (rules.md) uyğun olaraq aktiv və önə çıxan kitabları gətiririk
        context['featured_books'] = Book.objects.filter(
            is_active=True, 
            is_featured=True
        ).prefetch_related('authors', 'categories')[:4] # Performance üçün prefetch
        
        # Ana kateqoriyaları gətiririk
        context['categories'] = Category.objects.filter(
            is_active=True, 
            parent=None
        ).order_by('order')[:8]
        
        return context