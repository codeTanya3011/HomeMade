from carts.models import Cart
import logging


logger = logging.getLogger(__name__)

def get_user_carts(request):
    if request.user.is_authenticated:
        logger.info(f"Authenticated user: {request.user.username}")
        carts = Cart.objects.filter(user=request.user).select_related('product')
        logger.info(f"Found {carts.count()} carts for user {request.user.username}")
    else:
        if not request.session.session_key:
            logger.info("Session key not found. Creating a new session.")
            request.session.create()
        else:
            logger.info(f"Session key exists: {request.session.session_key}")
        
        carts = Cart.objects.filter(session_key=request.session.session_key).select_related('product')
        logger.info(f"Found {carts.count()} carts for session key: {request.session.session_key}")

    return carts
