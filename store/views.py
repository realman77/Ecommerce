from django.db.models import Count
from django.shortcuts import render, aget_object_or_404
from django.template.response import TemplateResponse
from django.views import View
from asgiref.sync import sync_to_async

from cart.models import Cart, CartItem
from category.models import Category
from .models import Product

# Create your views here.


# # First method
# class ProductsView(View):
#     async def get(self, request):
#         products = await sync_to_async(Product.objects.filter)(is_available=True)
#         context = {
#             "products": products,
#         }
#         return TemplateResponse(request, "home.html", context)
    

# # Second method
# class ProductsView(View):
#     async def get(self, request):
#         # Fetch products asynchronously and immediately evaluate the queryset
#         products = await sync_to_async(list)(Product.objects.filter(is_available=True))
        
#         context = {
#             "products": products,
#         }
        
#         return render(request, "home.html", context)

class StoreView(View):
    async def get(self, request, category_slug=None) -> TemplateResponse:
        if category_slug:
            category = await aget_object_or_404(Category, slug=category_slug)
            products = await sync_to_async(Product.objects.filter)(category=category, is_available=True)
            featured = products.alias(total=Count('cartitem')).filter(total__gt=0)
        if category_slug is None:
            products = await sync_to_async(Product.objects.filter)(is_available=True)
            featured = products.alias(total=Count('cartitem')).filter(total__gt=0)
        context = {
            "products": products,
            'featured': featured,
            'count': await sync_to_async(products.count)(),
            }
        return TemplateResponse(request, 'store.html', context)


class IndexView(View):
    async def get(self, request):
        return TemplateResponse(request, "index.html")
    

class ProductDetailView(View):
    async def get_cart(self, request):
        cart = request.session.session_key
        if cart:
            return cart
        cart = None
        return cart

    async def get(self, request, product_slug):
        product = await aget_object_or_404(Product, slug=product_slug)
        try:
            cart = await Cart.objects.aget(session_id=await self.get_cart(request))
        except Cart.DoesNotExist:
            cart = None
        try:
            cart_item = await CartItem.objects.aget(product=product, cart=cart)
            cart_item = await sync_to_async(CartItem.objects.filter(cart__session_id=await self.get_cart(request)).exists)()
            print(cart_item)
        except CartItem.DoesNotExist:
            cart_item = None
        context = {
            'product': product,
            "sizes": product.size.all(),
            "colors": product.color.all(),
            'featured': cart_item,
            }
        return TemplateResponse(request, "product-detail.html", context)