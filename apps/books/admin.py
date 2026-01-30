from django.contrib import admin
from .models import Category, Author, Book, Publisher

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'is_active', 'order')
    list_filter = ('is_active', 'parent')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'bio')
    prepopulated_fields = {'slug': ('name',)}

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
