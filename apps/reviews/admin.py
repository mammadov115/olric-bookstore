from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'is_verified_purchase', 'is_active', 'created_at')
    list_filter = ('rating', 'is_verified_purchase', 'is_active', 'created_at')
    search_fields = ('book__title', 'user__username', 'comment')
    actions = ['approve_reviews', 'disapprove_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_active=True)
    approve_reviews.short_description = "Approve selected reviews"

    def disapprove_reviews(self, request, queryset):
        queryset.update(is_active=False)
    disapprove_reviews.short_description = "Disapprove selected reviews"
