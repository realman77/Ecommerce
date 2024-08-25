from django.urls import path

from .views import *


urlpatterns = [
    path("", StoreView.as_view(), name="store"),
    path('category/<slug:category_slug>', StoreView.as_view(), name='category_slug'),
    path('index/', IndexView.as_view(), name="index"),
    path('product_detail/<slug:product_slug>', ProductDetailView.as_view(), name='product_slug')
]