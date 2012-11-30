from django.contrib import admin
from models import CartItem, Cart

class CartAdmin(admin.ModelAdmin):
    model = CartItem
    list_display = ('cart_id', 'date_added', 'article', 'pattern', 'color', 'size', 'quantity',)
    list_filter = ('cart_id', 'date_added',)
    list_per_page = 20
    ordering = ['cart_id', 'date_added',]

admin.site.register(CartItem, CartAdmin)
admin.site.register(Cart)

  