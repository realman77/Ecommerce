
from django.urls import path
from .views import *

urlpatterns = [
    path("", cart,name="cart"),
    path("add_product/<int:product_id>/", add_cart,name="cart_add"),
    path("sub_product/<int:cart_item_pk>/", sub_cart,name="cart_sub"),
    path('increment/<int:cart_item_pk>/', increment_cart, name="increment_cart"),
    path('remove/<int:pk>/', remove, name="cart_remove") 
]