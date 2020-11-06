from app.models import Cart, CartItem
from django.db.models import Sum

def cart_items_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request.no_of_cartItems = 0
        if request.user.is_authenticated == True:
            carts = Cart.objects.filter(user_id=request.user.id).order_by('-created_on')
            if carts.exists():
                cart=carts[0]
                no_of_cartItems = cart.cartitem_set.aggregate(Sum('quantity'))['quantity__sum']
                request.no_of_cartItems = no_of_cartItems
        
        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
