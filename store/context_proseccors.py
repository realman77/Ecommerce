
from django.core.exceptions import ObjectDoesNotExist
from cart.models import Cart, CartItem
from cart.views import _cart_id
def counter(request):
    
    try:
        cart = Cart.objects.get(session_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
        count = 0
        for item in cart_items:
            count += item.quantity
    except ObjectDoesNotExist:
        count = 0
    return dict (count=count)
