import asyncio
from asgiref.sync import sync_to_async
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import classonlymethod
from django.views import View
from django.template.response import TemplateResponse
from django.contrib.auth.views import redirect_to_login

from cart.models import Cart, CartItem
from store.models import Product

# Create your views here.

class CartView(View):
    def get(self, request, total=0, tax=0, gen_total=0):
        
        if not request.user.is_authenticated:
            return redirect("signin")
        cart_items = ''
        try:
            sample = AddCartView()
            cart = Cart.objects.get(session_id=sample._cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart)
            gen_total = sum([i.quantity * i.product.price for i in cart_items])
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
    def _cart_id(self, request):
        cart = request.session.session_key
        if not cart:
            cart = request.session.create()
        return cart
    
    # add_cart()
    def get(self, request, product_id):

        product = get_object_or_404(Product, id=product_id)
        if product.stock:
            try:
                cart = Cart.objects.get(session_id=self._cart_id(request))
            except Cart.DoesNotExist:
                cart = Cart.objects.create(session_id=self._cart_id(request))
            
            cart.save()

            try:
                cart_item = CartItem.objects.get(product=product, cart=cart)
                cart_item.quantity += 1
                cart_item.save()
            except CartItem.DoesNotExist:
                cart_item = CartItem.objects.create(
                    product=product,
                    cart=cart,
                    quantity=1)
                cart_item.save()
            
        return redirect(request.META.get("HTTP_REFERER", ""))
        # else:
        #     return redirect("store")
    

class SubtractCartView(View):
    def get(self, request, product_id,):
        product = get_object_or_404(Product, id=product_id)
        sample = AddCartView()
        cart = get_object_or_404(Cart, session_id=sample._cart_id(request))
        cart_item = get_object_or_404(CartItem, product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect("cart")
    

class DeleteCartView(View):
    def get(self, request, product_id,):
        product = get_object_or_404(Product, id=product_id)
        sample = AddCartView()
        cart = get_object_or_404(Cart, session_id=sample._cart_id(request))
        cart_item = get_object_or_404(CartItem, product=product, cart=cart)   
        cart_item.delete()
        return redirect("cart")