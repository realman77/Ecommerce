from django.urls import path
from .views import *


urlpatterns = [
    
    path("s/search/",search, name="search"),
    path("<slug:category_slug>/<slug:product_slug>/",product_slug,name="product_detail"),
    path("<slug:category_slug>/",store,name="products_by_category"),
    path("",store,name="store")
]
