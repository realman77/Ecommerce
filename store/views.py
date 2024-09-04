import keyword
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render
from django.template.response import TemplateResponse
from django.views import View
from asgiref.sync import sync_to_async

from cart.models import Cart, CartItem
from cart.views import AddCartView
from category.models import Category
from .models import Product
from django.core.paginator import Paginator
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
    def get(self, request, category_slug=None) -> TemplateResponse:
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = Product.objects.filter(category=category, is_available=True)
        if category_slug is None:
            products = Product.objects.filter(is_available=True)
        per_page = 3
        paginator = Paginator(products, per_page)
        page_num = request.GET.get("page")
        paged_products = paginator.get_page(page_num)
        print('---------------------------------------------------------------')
        print(paginator)
        context = {
            "products": paged_products,
            'count': per_page,
            }
        return TemplateResponse(request, 'store.html', context)


class IndexView(View):
    def get(self, request):
        return TemplateResponse(request, "index.html")
    

class ProductDetailView(View):
    def get_cart(self, request):
        cart = request.session.session_key
        if cart:
            return cart
        cart = None
        return cart

    def get(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        # color_var = product.variation_set.color()
        try:
            cart = Cart.objects.get(session_id=self.get_cart(request))
        except Cart.DoesNotExist:
            cart = None
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item = CartItem.objects.filter(cart__session_id=self.get_cart(request)).exists()
            print(cart_item)
        except CartItem.DoesNotExist:
            cart_item = None
        context = {
            'product': product,
            "sizes": product.size.all(),
            "colors": product.color.all(),
            'featured': cart_item,
            # "color_var": color_var,
            }
        return TemplateResponse(request, "product-detail.html", context)
    

class SearchView(View):

    def get(self, request):
        keyword = request.GET.get("keyword", "")
        products = Product.objects.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword))
        print('-----------------------------------------------------------------')
        # print(products)
        context = {
            "products": products,
            'count': products.count(),
            'keyword': keyword
            }
        
        return TemplateResponse(request, "store.html", context)