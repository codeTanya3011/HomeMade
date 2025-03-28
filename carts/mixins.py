from django.template.loader import render_to_string
from django.urls import reverse
from carts.models import Cart
from carts.utils import get_user_carts
from django.db.models import Sum
import logging

# Configure the logger
logger = logging.getLogger(__name__)

class CartMixin:
    def get_cart(self, request, product=None, cart_id=None):
        query_kwargs = {}

        if request.user.is_authenticated:
            query_kwargs["user"] = request.user
        else:
            if not request.session.session_key:
                request.session.create() 
            query_kwargs["session_key"] = request.session.session_key

        logger.info(f"Getting cart for session_key: {request.session.session_key}, user: {request.user}")

        if product:
            query_kwargs["product"] = product
        if cart_id:
            query_kwargs["id"] = cart_id

        try:
            cart = Cart.objects.filter(**query_kwargs).first()
            logger.info(f"Cart retrieved: {cart}")
            return cart
        except Cart.DoesNotExist:
            logger.warning("Cart not found")
            return None

    def get_total_quantity(self, request):
        """Отримуємо загальну кількість товарів"""
        query_kwargs = {}

        if request.user.is_authenticated:
            query_kwargs["user"] = request.user
        else:
            query_kwargs["session_key"] = request.session.session_key

        total = Cart.objects.filter(**query_kwargs).aggregate(total=Sum("quantity"))["total"]
        total_quantity = total or 0
        logger.info(f"Total quantity in cart: {total_quantity}") 
        return total_quantity

    def render_cart(self, request):
        """Оновлюємо HTML-код кошика"""
        user_cart = get_user_carts(request)

        logger.info(f"User carts: {list(user_cart.values())}")
        
        context = {"carts": user_cart, "total_quantity": self.get_total_quantity(request)}

        referer = request.META.get("HTTP_REFERER", "")
        if reverse("orders:create_order") in referer:
            context["order"] = True

        logger.info("Rendering cart HTML update")
        return render_to_string("carts/includes/included_cart.html", context, request=request)






# class CartMixin:
#     def get_cart(self, request, product=None, cart_id=None):
#         if request.user.is_authenticated:
#             return Cart.objects.filter(user=request.user, product=product).first()

#         session_key = request.session.session_key
#         if not session_key:
#             return None 
        
#         if cart_id:
#             return Cart.objects.filter(session_key=session_key, id=cart_id).first()
        
#         return Cart.objects.filter(session_key=session_key, product=product).first()

