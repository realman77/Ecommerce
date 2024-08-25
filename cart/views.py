from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.views import View
from django.template.response import TemplateResponse

from cart.models import Cart, CartItem
from store.models import Product

# Create your views here.

class CartView(View):
    async def get(self, request):
        cart_items = ''
        try:
            sample = AddCartView()
            cart = await Cart.objects.aget(session_id=await sample._cart_id(request))
            cart_items = await sync_to_async(CartItem.objects.filter)(cart=cart)
        except ObjectDoesNotExist:
            pass
        context = {
            'cart_items': cart_items
            }
        return TemplateResponse(request, "cart.html", context)


class AddCartView(View):
    async def _cart_id(self, request):
        cart = request.session.session_key
        if not cart:
            cart = await request.session.acreate()
        return cart
    
    # add_cart()
    async def get(self, request, product_id):
        product = await Product.objects.aget(id=product_id)

        try:
            cart = await Cart.objects.aget(session_id=await self._cart_id(request))
        except Cart.DoesNotExist:
            cart = await Cart.objects.acreate(session_id=await self._cart_id(request))
        
        await cart.asave()

        try:
            cart_item = await CartItem.objects.aget(product=product, cart=cart)
            cart_item.quantity += 1
            await cart_item.asave()
        except CartItem.DoesNotExist:
            cart_item = await CartItem.objects.acreate(
                product=product,
                cart=cart,
                quantity=1)
            await cart_item.asave()
        
        return redirect("cart")