from django.urls import path

from place_order.views import PlaceOrderView


urlpatterns = [
    path("", PlaceOrderView.as_view(), name="place-order"),
]