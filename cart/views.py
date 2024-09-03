import asyncio
from asgiref.sync import sync_to_async
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, aget_object_or_404
from django.utils.decorators import classonlymethod
from django.views import View
from django.template.response import TemplateResponse
from django.contrib.auth.views import redirect_to_login

from cart.models import Cart, CartItem
from store.models import Product

# Create your views here.

class CartView(View):
    async def get(self, request, total=0, tax=0, gen_total=0):
        
        if not await sync_to_async(lambda: request.user.is_authenticated)():
            return redirect("signin")
        cart_items = ''
        try:
            sample = AddCartView()
            cart = await Cart.objects.aget(session_id=await sample._cart_id(request))
            cart_items = await sync_to_async(CartItem.objects.filter)(cart=cart)
            gen_total = sum([i.quantity * await sync_to_async(lambda: i.product.price)() async for i in cart_items])
            print('--------------------------------------------------------------------------------------------------------------------')
            print(gen_total)
            tax = gen_total/ 100 * 2
            total = gen_total - tax
        except ObjectDoesNotExist:
            pass
        context = {
            'cart_items': cart_items,
            'total': total,
            'tax': tax,
            'gen_total': gen_total,
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

        product = await aget_object_or_404(Product, id=product_id)
        if product.stock:
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
            
        return redirect(request.META.get("HTTP_REFERER", ""))
        # else:
        #     return redirect("store")
    

class SubtractCartView(View):
    async def get(self, request, product_id,):
        product = await aget_object_or_404(Product, id=product_id)
        sample = AddCartView()
        cart = await aget_object_or_404(Cart, session_id=await sample._cart_id(request))
        cart_item = await aget_object_or_404(CartItem, product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            await cart_item.asave()
        else:
            await cart_item.adelete()
        return redirect("cart")
    

class DeleteCartView(View):
    async def get(self, request, product_id,):
        product = await aget_object_or_404(Product, id=product_id)
        sample = AddCartView()
        cart = await aget_object_or_404(Cart, session_id=await sample._cart_id(request))
        cart_item = await aget_object_or_404(CartItem, product=product, cart=cart)   
        await cart_item.adelete()
        return redirect("cart")