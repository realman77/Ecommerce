
from itertools import product
from multiprocessing import context
from django.shortcuts import get_object_or_404, render


from category.models import Category
from store.models import Product

# Create your views here.
def store(request,category_slug=None):
    if category_slug == None:   
        products = Product.objects.filter(is_available=True)
    else:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(is_available=True,category=categories)
    context = {
        "products": products,
        "product_count": products.count(),
    }
    return render(request, "store.html",context)

def product_slug(request,category_slug,product_slug):
    product = get_object_or_404(Product,slug=product_slug,category__slug=category_slug)
    context = {
        "product": product,
    }
    return render(request, "product_detail.html",context)    