from django.contrib import admin
from models import OrderItem, ReaOrderItem

class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    list_display = ('checkout', )
    list_display_links = ('checkout',)
    list_filter = ('checkout',)
    list_per_page = 20

class ReaOrderItemAdmin(admin.ModelAdmin):
    model = ReaOrderItem
    list_display = ('checkout', )
    list_display_links = ('checkout',)
    list_filter = ('checkout',)
    list_per_page = 20


admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ReaOrderItem, ReaOrderItemAdmin)
