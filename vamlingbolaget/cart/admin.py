from django.contrib import admin
from models import *

class CartAdmin(admin.ModelAdmin):
    model = CartItem

admin.site.register(CartItem, CartAdmin)    
