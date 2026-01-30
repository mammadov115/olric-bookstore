from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ['book']
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at', 'total_items_count')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    inlines = [CartItemInline]
    
    def total_items_count(self, obj):
        return obj.items.count()
    total_items_count.short_description = 'Items'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'book', 'quantity', 'price_at_addition')
    raw_id_fields = ('cart', 'book')
