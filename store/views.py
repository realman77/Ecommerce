


from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.db.models import Q
from cart.models import CartItem
from category.models import Category
from store.models import Product
from cart.views import _cart_id
# Create your views here.
def store(request,category_slug=None):
    if category_slug == None:   
        products = Product.objects.filter(is_available=True)
    else:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(is_available=True,category=categories)

    # Paginator
    paginator = Paginator(products, 3)
    page_num = request.GET.get("page")
    paged_product = paginator.get_page(page_num)


    context = {
        "products": paged_product,
        "product_count": products.count(),
    }
    return render(request, "store.html",context)

def product_slug(request,category_slug,product_slug):
    product = get_object_or_404(Product,slug=product_slug,category__slug=category_slug)
    cart_in = CartItem.objects.filter(cart__session_id = _cart_id(request)).exists()
    context = {
        "product": product,
        "cart_in": cart_in,
    }
    return render(request, "product_detail.html",context)  
  
def search(request):
    keyword = request.GET.get("keyword", "").strip()  # Bo'sh joylarni olib tashlash
    products = Product.objects.none()  # Standart bo'sh queryset

    if keyword:  # Faqat keyword mavjud bo'lsa filtr qo'llanadi
        products = Product.objects.filter(
            Q(name__icontains=keyword) | Q(description__icontains=keyword)
        )
    
    context = {
        "products": products,
        "product_count": products.count(),
    }
    return render(request, 'store.html', context)
