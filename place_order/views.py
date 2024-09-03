from django.shortcuts import render
from django.views import View
from django.template.response import TemplateResponse


# Create your views here.

class PlaceOrderView(View):
    async def get(self, request):
        return TemplateResponse(request, "place-order.html")