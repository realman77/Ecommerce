from django.contrib import admin

from cart.models import *

# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_id', "date_added",)
    list_display_links = ('id', 'session_id', "date_added",)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'cart', 'quantity', 'is_active')
    list_display_links = ("id", 'product', 'cart', 'quantity', 'is_active')


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)