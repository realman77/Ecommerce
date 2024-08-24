from django.urls import path

from store.views import *


urlpatterns = [
    path('', ProductsView.as_view(), name=""),

]