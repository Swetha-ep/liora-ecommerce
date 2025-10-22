from orders.models import Cart

def cart_context(request):
    cart_count = 0
    cart_total = 0

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.items.count()
            cart_total = cart.total_price
        except Cart.DoesNotExist:
            pass
    
    return {
        'cart_count' : cart_count,
        'cart_total' : cart_total
    }