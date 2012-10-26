from django.contrib import admin
from models import CartItem, Cart

class CartAdmin(admin.ModelAdmin):
    model = CartItem
    list_display = ('cart', 'date_added', 'article', 'pattern', 'color', 'size', 'quantity',)
    list_filter = ('cart', 'date_added',)
    list_per_page = 20
    ordering = ['cart', 'date_added',]

admin.site.register(CartItem, CartAdmin)
admin.site.register(Cart)

  