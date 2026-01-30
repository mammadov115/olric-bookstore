from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import get_object_or_404
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

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        queryset = Book.objects.filter(is_active=True).prefetch_related('authors', 'categories')
        
        # Filtering by category if provided in URL or query params
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(categories=self.category)
        else:
            self.category = None
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_categories'] = Category.objects.filter(is_active=True, parent=None).prefetch_related('children')
        context['current_category'] = self.category
        return context

class CategoryBrowseView(ListView):
    model = Category
    template_name = 'books/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.filter(is_active=True, parent=None).prefetch_related('children')

class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_queryset(self):
        return Book.objects.filter(is_active=True).prefetch_related('authors', 'categories', 'publisher')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Related books (from same category)
        first_category = self.object.categories.first()
        if first_category:
            context['related_books'] = Book.objects.filter(
                is_active=True, 
                categories=first_category
            ).exclude(id=self.object.id).prefetch_related('authors')[:4]
        return context