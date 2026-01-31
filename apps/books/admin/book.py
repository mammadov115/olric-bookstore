from django.contrib import admin
from apps.books.models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'discount_price', 'stock', 'is_active', 'is_featured', 'created_at')
    list_filter = ('is_active', 'is_featured', 'categories', 'format')
    search_fields = ('title', 'isbn', 'authors__name')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['authors', 'categories']
    # inlines = [BookImageInline]
    readonly_fields = ('views_count',)
    
    fieldsets = (
        ('General Info', {
            'fields': ('title', 'slug', 'authors', 'categories', 'format', 'isbn')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'discount_price', 'stock')
        }),
        ('Details', {
            'fields': ('description', 'cover_image', 'pages', 'language', 'publication_date', 'publisher')
        }),
        ('Settings', {
            'fields': ('is_active', 'is_featured', 'views_count')
        }),
    )
