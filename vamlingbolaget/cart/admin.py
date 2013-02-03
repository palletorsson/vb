from django.contrib import admin
from models import CartItem, Cart, BargainCartItem

class CartAdmin(admin.ModelAdmin):
    model = CartItem
    list_display = ('cart', 'date_added', 'article', 'pattern', 'color', 'size', 'quantity', 'id', 'pk')
    list_filter = ('cart', 'date_added',)
    list_per_page = 5
    ordering = ['cart', 'date_added',]

admin.site.register(CartItem, CartAdmin)
admin.site.register(Cart)
admin.site.register(BargainCartItem)

