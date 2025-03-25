from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from carts.mixins import CartMixin

from carts.models import Cart
from carts.utils import get_user_carts
from goods.models import Products

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View
from .models import Cart, Products

from django.http import JsonResponse
from django.template.loader import render_to_string
import logging


logger = logging.getLogger(__name__)

class CartAddView(CartMixin, View):
    def post(self, request):
        product_id = request.POST.get("product_id")
        logger.info(f"Received request to add product {product_id} to cart") 

        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            logger.error(f"Product {product_id} not found") 
            return JsonResponse({"success": False, "message": "Product not found"}, status=404)

        if not request.session.session_key:
            request.session.create()

        cart = self.get_cart(request, product=product)

        if cart:
            cart.quantity += 1
            cart.save()
            logger.info(f"Updated cart item: {cart}") 
        else:
            Cart.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key if not request.user.is_authenticated else None,
                product=product, 
                quantity=1
            )
            logger.info(f"Created new cart item for product {product_id}")

        total_quantity = self.get_total_quantity(request)

        cart_items_html = self.render_cart(request)

        response_data = {
            "success": True,
            "message": "Product added to cart!",
            "total_quantity": total_quantity,  
            "cart_items_html": cart_items_html
        }

        logger.info(f"Response data: {response_data}")
        return JsonResponse(response_data)


logger = logging.getLogger(__name__)

class CartChangeView(CartMixin, View):
    def post(self, request):
        logger.info("CartChangeView: Received a request to change the cart.")

        cart_id = request.POST.get("cart_id")
        cart = self.get_cart(request, cart_id=cart_id)

        if not cart:
            logger.warning(f"Cart with ID {cart_id} not found.")
            return JsonResponse({"message": "Cart not found"}, status=404)

        new_quantity = int(request.POST.get("quantity", 1))
        logger.info(f"Updating cart item with ID {cart.id} to new quantity: {new_quantity}")

        cart.quantity = max(1, new_quantity)
        cart.save()

        logger.info(f"Updated cart item with ID {cart.id}, new quantity: {cart.quantity}")

        response_data = {
            "message": "Quantity changed",
            "quantity": cart.quantity,
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)


logger = logging.getLogger(__name__)

class CartRemoveView(CartMixin, View):
    def post(self, request):
        logger.info("CartRemoveView: Received a request to remove an item from the cart.")

        cart_id = request.POST.get("cart_id")
        cart = self.get_cart(request, cart_id=cart_id)

        if not cart:
            logger.warning(f"Cart item with ID {cart_id} not found for removal.")
            return JsonResponse({"message": "Product not found in cart"}, status=404)

        quantity = cart.quantity
        logger.info(f"Removing cart item with ID {cart.id}, quantity: {quantity}")

        cart.delete()

        logger.info(f"Successfully removed cart item with ID {cart.id}.")

        response_data = {
            "message": "Product removed from cart",
            "quantity_deleted": quantity,
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)




# def cart_add(request):

#     product_id = request.POST.get("product_id")
#     product = Products.objects.get(id=product_id)
#     if request.user.is_authenticated:
#         carts = Cart.objects.filter(user=request.user, product=product)
#         if carts.exists():
#             cart = carts.first()
#             if cart:
#                 cart.quantity += 1
#                 cart.save()
#         else:
#             Cart.objects.create(user=request.user, product=product, quantity=1)
#     else:
#         carts = Cart.objects.filter(
#             session_key=request.session.session_key, product=product)
#         if carts.exists():
#             cart = carts.first()
#             if cart:
#                 cart.quantity += 1
#                 cart.save()
#         else:
#             Cart.objects.create(
#                 session_key=request.session.session_key, product=product, quantity=1)
#     user_cart = get_user_carts(request)
#     cart_items_html = render_to_string(
#         "carts/includes/included_cart.html", {"carts": user_cart}, request=request)

#     response_data = {
#         "message": "",
#         "cart_items_html": cart_items_html,
#     }
#     return JsonResponse(response_data)

# def cart_change(request):

#     cart_id = request.POST.get("cart_id")
#     quantity = request.POST.get("quantity")

#     cart = Cart.objects.get(id=cart_id)
    
#     cart.quantity = quantity
#     cart.save()
#     updated_quantity = cart.quantity
    
#     user_cart = get_user_carts(request)
#     context = {"carts": user_cart}

#     # if referer page is create_order add key orders: True to context
#     referer = request.META.get('HTTP_REFERER')
#     if reverse('orders:create_order') in referer:
#         context["orders"] = True
#     cart_items_html = render_to_string(
#         "carts/includes/included_cart.html", context, request=request)

#     response_data = {
#         "message": "",
#         "cart_items_html": cart_items_html,
#         "quantity": updated_quantity,
#     }
#     return JsonResponse(response_data)

# def cart_remove(request):

#     cart_id = request.POST.get("cart_id")
    
#     cart = Cart.objects.get(id=cart_id)
#     quantity = cart.quantity
#     cart.delete()
    
#     user_cart = get_user_carts(request)
#     context = {"carts": user_cart}

#     # if referer page is create_order add key orders: True to context
#     referer = request.META.get('HTTP_REFERER')
#     if reverse('orders:create_order') in referer:
#         context["orders"] = True

#     cart_items_html = render_to_string(
#          "carts/includes/included_cart.html", context, request=request)
#     response_data = {
#         "message": "",
#         "cart_items_html": cart_items_html,
#         "quantity_deleted": quantity,
#     }
#     return JsonResponse(response_data)
