from django.views.generic import DetailView
from apps.books.models import Book
from apps.reviews.forms import ReviewForm

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
            context['related_books'] = Book.objects.with_stats().filter(
                is_active=True, 
                categories=first_category
            ).exclude(id=self.object.id).prefetch_related('authors')[:4]
            
        context['review_form'] = ReviewForm()
        return context
