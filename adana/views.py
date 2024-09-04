from django.shortcuts import redirect
from django.views import View
from django.template.response import TemplateResponse

from store.models import Product


# First method
class ProductsView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("signin")
        products = Product.objects.filter(is_available=True)
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


