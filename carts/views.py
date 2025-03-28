from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from carts.mixins import CartMixin
from django.shortcuts import get_object_or_404
from django.db.models import Sum, F

from carts.models import Cart
from carts.utils import get_user_carts
from goods.models import Products

from .models import Cart, Products
import logging


logger = logging.getLogger(__name__)

class CartAddView(CartMixin, View):
    def post(self, request):
        product_id = request.POST.get("product_id")
        logger.info(f"CartAddView Received request to add product {product_id} to cart")  

        product = get_object_or_404(Products, id=product_id)

        # Перевірка на session_key
        if not request.session.session_key:
            request.session.create()

        logger.info(f"Session key before adding to cart: {request.session.session_key}")

        # Отримуємо корзину
        cart = self.get_cart(request, product=product)

        if cart:
            cart.quantity += 1
            cart.save()
            logger.info(f"Updated cart item: {cart}")  
        else:
            cart = Cart.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key if not request.user.is_authenticated else None,
                product=product, 
                quantity=1
            )
            logger.info(f"Created new cart item for product {product_id}")

        total_quantity = self.get_total_quantity(request)

        cart_items_html = self.render_cart(request)

        logger.info(f"Cart HTML update: {cart_items_html}")

        response_data = {
            "success": True,
            "message": f"{product.name} added to cart!",
            "total_quantity": total_quantity,
            "cart_items_html": cart_items_html
        }

        logger.info(f"CartAddView Cart updated successfully. Response: {response_data}")
        return JsonResponse(response_data)


logger = logging.getLogger(__name__)

class CartChangeView(CartMixin, View):
    def post(self, request):
        logger.info("CartChangeView: Request to change cart received")

        cart_id = request.POST.get("cart_id")
        cart = self.get_cart(request, cart_id=cart_id)

        if not cart:
            logger.warning(f"Cart with ID {cart_id} not found")
            return JsonResponse({"message": "Cart not found"}, status=404)

        new_quantity = int(request.POST.get("quantity", 1))
        logger.info(f"We update the quantity of goods in the cart with ID {cart.id} to the new quantity: {new_quantity}")

        cart.quantity = max(1, new_quantity)
        cart.save()

        logger.info(f"Cart with ID {cart.id} updated, new quantity: {cart.quantity}")

        total_price = Cart.objects.filter(user=request.user).total_price()
        total_quantity = Cart.objects.filter(user=request.user).total_quantity()

        # Кошик після оновлення
        carts = Cart.objects.filter(user=request.user)
        
        for item in carts:
            item.product_price = item.products_price()

        cart_items_html = render_to_string("carts/includes/included_cart.html", {
            "carts": carts,
            "total_price": total_price, 
            "total_quantity": total_quantity 
        })

        response_data = {
            "message": "Количество изменено",
            "quantity": cart.quantity,
            "cart_price": cart.products_price(),
            "total_price": total_price,
            "total_quantity": total_quantity,
            "cart_items_html": cart_items_html,
        }
        return JsonResponse(response_data)


logger = logging.getLogger(__name__)

class CartRemoveView(View):
    def post(self, request):

        cart_id = request.POST.get("cart_id")
        
        if not cart_id:
            return JsonResponse({"message": "Cart ID is missing"}, status=400)

        cart_item = get_object_or_404(Cart, id=cart_id)

        logger.info(f"Removing cart item with ID {cart_item.id}, quantity: {cart_item.quantity}")

        # Видалення товару з корзини
        cart_item.delete()

        logger.info(f"Successfully removed cart item with ID {cart_item.id}")

        total_price = Cart.objects.filter(user=request.user).annotate(
            total_item_price=F('product__price') * F('quantity')
        ).aggregate(Sum('total_item_price'))['total_item_price__sum']

        total_quantity = Cart.objects.filter(user=request.user).aggregate(Sum('quantity'))['quantity__sum']

        response_data = {
            "message": "Item removed successfully",
            "total_price": total_price if total_price else 0,
            "total_quantity": total_quantity if total_quantity else 0,
            "cart_items_html": self.render_cart(request),
        }

        return JsonResponse(response_data)

    def render_cart(self, request):

        carts = Cart.objects.filter(user=request.user)
        return render_to_string("carts/includes/included_cart.html", {"carts": carts})





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
