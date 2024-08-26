from asgiref.sync import async_to_sync
from django.db.models import QuerySet, Count
from django.http import QueryDict
from django.shortcuts import render

from cart.models import Cart, CartItem
from cart.views import AddCartView

from .models import Category


def menu_links(request):
    sample = AddCartView()
    categories = Category.objects.alias(total=Count('product')).filter(total__gt=0)
    try:
        cart = Cart.objects.get(session_id=async_to_sync(sample._cart_id)(request))
    except Cart.DoesNotExist:
        cart = None
    cart_item = CartItem.objects.filter(cart=cart)
    cart_count = sum([i.quantity for i in cart_item])
    context = {
        'categories': categories,
        'cart_count': cart_count,
    }
    print(context)
    return context
