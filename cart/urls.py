from django.urls import path

from cart.views import *


urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path('add_product/<int:product_id>', AddCartView.as_view(), name='add_cart'),
]