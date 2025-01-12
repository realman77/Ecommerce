import django.db
from django.shortcuts import redirect, render,get_object_or_404

from cart.models import Cart, CartItem
from store.models import Product, Variation
from django.db.models import Count
# Create your views here.

def cart(request,total = 0,tax=0,gen_total=0,cart_items=None):
    try:
        cart = Cart.objects.get(session_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
        
        for cart_item in cart_items:
            total += cart_item.quantity * cart_item.product.price
        tax = (total*2)/100
        gen_total = total - tax
    except Cart.DoesNotExist:
        pass
    context = {
        "cart_items":cart_items,
        "total":total,
        "tax":tax,
        "gen_total":gen_total,
    }
    return render(request, "cart.html",context)

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    # Mahsulotni olish
    product = Product.objects.get(id=product_id)

    # POST ma'lumotlarini o'qish
    data = {key: value[0] for key, value in request.POST.lists()}
    data.pop('csrfmiddlewaretoken', None)

    # Variationsni yig‘ish
    variations = []
    for category, value in data.items():
        variation = Variation.objects.get(product=product, category=category, value=value)
        variations.append(variation)

    # Savatni olish yoki yaratish
    try:
        cart = Cart.objects.get(session_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(session_id=_cart_id(request))
    cart.save()

    # CartItemni boshqarish
    try:
        # Filtrlash va birinchi mos keladigan obyektni olish
        cart_items = (
            CartItem.objects.filter(product=product, cart=cart)
            .annotate(num=Count('variations'))
            .filter(num=len(variations), variations__in=variations)
        )

        if cart_items.exists():
            cart_item = cart_items.first()
            cart_item.quantity += 1
            cart_item.save()
        else:
            raise CartItem.DoesNotExist

    except CartItem.DoesNotExist:
        # Yangi CartItem yaratish
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        cart_item.variations.set(variations)
        cart_item.save()

    return redirect('cart')
from django.db.models import Count
from django.shortcuts import redirect

from django.db.models import Count
from django.shortcuts import redirect

def add_cart(request, product_id):
    # Mahsulotni olish
    product = Product.objects.get(id=product_id)

    # POST ma'lumotlarini o‘qish
    data = {key: value[0] for key, value in request.POST.lists()}
    data.pop('csrfmiddlewaretoken', None)

    # Variationsni yig‘ish
    variations = []
    for category, value in data.items():
        variation = Variation.objects.get(product=product, category=category, value=value)
        variations.append(variation)

    # Savatni olish yoki yaratish
    try:
        cart = Cart.objects.get(session_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(session_id=_cart_id(request))
    cart.save()

    # CartItemni boshqarish
    try:
        # Filter orqali to‘g‘ri obyektni topish
        cart_items = CartItem.objects.filter(product=product, cart=cart)

        # Har bir cart_itemning variatsiyalarini solishtirish
        cart_item = None
        for item in cart_items:
            if set(item.variations.all()) == set(variations):  # To‘liq moslikni tekshirish
                cart_item = item
                break

        if cart_item:
            # Agar obyekt topilgan bo‘lsa, uning quantity ni oshirish
            cart_item.quantity += 1
            cart_item.save()
        else:
            raise CartItem.DoesNotExist

    except CartItem.DoesNotExist:
        # Yangi CartItem yaratish
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        cart_item.variations.set(variations)
        cart_item.save()

    return redirect('cart')

# Dublikatlarni tozalash funksiyasi (faqat kerak bo‘lganda chaqiring)
def sub_cart(request, cart_item_pk):
    cart_item = CartItem.objects.get(pk=cart_item_pk)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def increment_cart(request, cart_item_pk):
    cart_item = CartItem.objects.get(pk=cart_item_pk)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

def remove(request, pk):    
    cart_item = CartItem.objects.get(pk=pk)
    cart_item.delete()
    return redirect('cart')