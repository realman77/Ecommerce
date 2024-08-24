from django.views import View
from asgiref.sync import sync_to_async
from django.template.response import TemplateResponse

from store.models import Product


# First method
class ProductsView(View):
    async def get(self, request):
        products = await sync_to_async(Product.objects.filter)(is_available=True)
        context = {
            "products": products,
        }
        return TemplateResponse(request, "home.html", context)
    

# # Second method
# class ProductsView(View):
#     async def get(self, request):
#         # Fetch products asynchronously and immediately evaluate the queryset
#         products = await sync_to_async(list)(Product.objects.filter(is_available=True))
        
#         context = {
#             "products": products,
#         }
        
#         return render(request, "home.html", context)


