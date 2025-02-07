from django.template.loader import render_to_string
from django.urls import reverse
from carts.models import Cart
from carts.utils import get_user_carts


class CartMixin:
    def get_cart(self, request, product=None, cart_id=None):
        query_kwargs = {}

        if request.user.is_authenticated:
            query_kwargs["user"] = request.user
        else:
            query_kwargs["session_key"] = request.session.session_key

        if product:
            query_kwargs["product"] = product
        if cart_id:
            query_kwargs["id"] = cart_id

        try:
            return Cart.objects.filter(**query_kwargs).first()
        except Cart.DoesNotExist:
            return None  # Or handle as needed

    def render_cart(self, request):
        user_cart = get_user_carts(request)  # Ensure this function is defined
        context = {"carts": user_cart}

        # Check if referer is from create_order page and add context variable
        referer = request.META.get('HTTP_REFERER', '')
        if reverse('orders:create_order') in referer:
            context["order"] = True

        return render_to_string(
            "carts/includes/included_cart.html", context, request=request
        )


# class CartMixin:
#     def get_cart(self, request, product=None, cart_id=None):
#         if request.user.is_authenticated:
#             return Cart.objects.filter(user=request.user, product=product).first()

#         session_key = request.session.session_key  # Проверяем текущую сессию
#         if not session_key:
#             return None  # Если нет session_key, корзина не найдена
        
#         if cart_id:
#             return Cart.objects.filter(session_key=session_key, id=cart_id).first()
        
#         return Cart.objects.filter(session_key=session_key, product=product).first()