import json
from django.shortcuts import get_object_or_404
from .models import CartItem
from main.models import Product

def merge_anonymous_cart_to_user(request, user):
    cart_str = request.COOKIES.get('cart', '{}')
    try:
        anon_cart = json.loads(cart_str)
    except json.JSONDecodeError:
        anon_cart = {}

    if not anon_cart:
        return

    for pid, data in anon_cart.items():
        try:
            product = Product.objects.get(id=int(pid))
            qty = data.get('quantity', 1)
            cart_item, created = CartItem.objects.get_or_create(
                user=user,
                product=product,
                defaults={'quantity': qty}
            )
            if not created:
                cart_item.quantity += qty
                cart_item.save()
        except Product.DoesNotExist:
            continue