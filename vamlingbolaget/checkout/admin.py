from django.contrib import admin
from models import Checkout

class CheckoutAdmin(admin.ModelAdmin):
    model = Checkout
    list_display = ('order_number', 'first_name', 'last_name', 'email', 'phone', 'status', 'paymentmethod', 'payex_key')
    list_display_links = ('order_number',)
    list_editable = ('status',)
    list_filter = ('order_number', 'first_name', 'last_name',)
    list_per_page = 20
    ordering = ['id',]

admin.site.register(Checkout, CheckoutAdmin)
