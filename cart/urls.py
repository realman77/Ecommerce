from django.urls import path

from cart.views import *


urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path('add_product/<int:product_id>', AddCartView.as_view(), name='add_cart'),
    path('sub_product/<int:item_id>', SubtractCartView.as_view(), name='sub_cart'),
    path('increment_product/<int:item_id>', IncrementCartView.as_view(), name='increment_cart'),
    path('del_product/<int:item_id>', DeleteCartView.as_view(), name='del_cart'),

]