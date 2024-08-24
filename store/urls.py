from django.urls import path

from store.views import *


urlpatterns = [
    # path('', ProductsView.as_view(), name=""),
    path('', pr, name="home"),
    path("store/", StoreView.as_view(), name="store"),
]