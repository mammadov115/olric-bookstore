from django.contrib import admin
from apps.books.models import Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'bio')
    prepopulated_fields = {'slug': ('name',)}
