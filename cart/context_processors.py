import json
from django.db.models import Sum
from .models import CartItem

def cart_count(request):
    if request.user.is_authenticated:
        total = CartItem.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total']
        count = total or 0
    else:
        try:
            cart_str = request.COOKIES.get('cart', '{}')
            cart = json.loads(cart_str)
            count = sum(item.get('quantity', 0) for item in cart.values())
        except json.JSONDecodeError:
            count = 0
    return {'cart_count': count}