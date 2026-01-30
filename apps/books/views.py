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
    context_object_name = 'books'
    paginate_by = 12

    def get_template_names(self):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['books/includes/book_list_content.html']
        return ['books/book_list.html']

    def get_queryset(self):
        from django.db.models import Q
        queryset = Book.objects.filter(is_active=True).prefetch_related('authors', 'categories')
        
        # 1. Full-text Search
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(authors__name__icontains=query) |
                Q(isbn__icontains=query)
            ).distinct()

        # 2. Category Filtering
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(categories=self.category)
        else:
            self.category = None
            
        # 3. Faceted Filtering
        author_id = self.request.GET.get('author')
        if author_id:
            queryset = queryset.filter(authors__id=author_id)
            
        book_format = self.request.GET.get('format')
        if book_format:
            queryset = queryset.filter(format=book_format)
            
        min_price = self.request.GET.get('min_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
            
        max_price = self.request.GET.get('max_price')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
            
        # 4. Sorting
        sort = self.request.GET.get('sort', '-created_at')
        allowed_sorts = ['price', '-price', '-created_at', '-views_count']
        if sort in allowed_sorts:
            queryset = queryset.order_by(sort)
            
        return queryset

    def get_context_data(self, **kwargs):
        from apps.books.models import Author
        context = super().get_context_data(**kwargs)
        context['all_categories'] = Category.objects.filter(is_active=True, parent=None).prefetch_related('children')
        context['current_category'] = self.category
        context['authors'] = Author.objects.all()[:20] # Top 20 authors for filter
        context['formats'] = Book.Format.choices
        
        # Keep track of active filters for UI state
        context['active_author'] = self.request.GET.get('author')
        context['active_format'] = self.request.GET.get('format')
        context['active_min_price'] = self.request.GET.get('min_price')
        context['active_max_price'] = self.request.GET.get('max_price')
        context['active_sort'] = self.request.GET.get('sort', '-created_at')
        context['search_query'] = self.request.GET.get('q', '')
        
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