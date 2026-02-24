from django.shortcuts import render, get_object_or_404  
from django.contrib import messages  
from django.http import HttpResponseRedirect  
from django.urls import reverse  
from decimal import Decimal  
from main.models import Product  
import json  

def add_to_cart(request, product_id):  
    if request.method == 'POST':  
        try:  
            cart_str = request.COOKIES.get('cart', '{}')  
            cart = json.loads(cart_str)  
        except json.JSONDecodeError:  
            cart = {}  

        pid = str(product_id)  
        product = get_object_or_404(Product, id=product_id)  
        if pid in cart:  
            cart[pid]['quantity'] += 1  
        else:  
            cart[pid] = {'quantity': 1}  

        response = HttpResponseRedirect(reverse('cart:cart_detail'))  
        response.set_cookie('cart', json.dumps(cart), max_age=60*60*24*30, httponly=True, samesite='Lax')  # 30 днів  
        messages.success(request, f'Товар «{product.name}» додано до корзини.')  
        return response  
    return HttpResponseRedirect(reverse('main:product_list'))  

def remove_from_cart(request, product_id):  
    if request.method == 'POST':  
        try:  
            cart_str = request.COOKIES.get('cart', '{}')  
            cart = json.loads(cart_str)  
        except json.JSONDecodeError:  
            cart = {}  

        pid = str(product_id)  
        if pid in cart:  
            del cart[pid]  

        response = HttpResponseRedirect(reverse('cart:cart_detail'))  
        response.set_cookie('cart', json.dumps(cart), max_age=60*60*24*30, httponly=True, samesite='Lax')  
        messages.success(request, 'Товар видалено з корзини.')  
        return response  
    return HttpResponseRedirect(reverse('cart:cart_detail'))  

def update_quantity(request, product_id):  
    if request.method == 'POST':  
        try:  
            cart_str = request.COOKIES.get('cart', '{}')  
            cart = json.loads(cart_str)  
        except json.JSONDecodeError:  
            cart = {}  

        pid = str(product_id)  
        try:  
            quantity = int(request.POST.get('quantity', 1))  
            if quantity < 1:  
                quantity = 1  
            if pid in cart:  
                cart[pid]['quantity'] = quantity  
        except ValueError:  
            pass  

        response = HttpResponseRedirect(reverse('cart:cart_detail'))  
        response.set_cookie('cart', json.dumps(cart), max_age=60*60*24*30, httponly=True, samesite='Lax')  
        return response  
    return HttpResponseRedirect(reverse('cart:cart_detail'))  

def cart_detail(request):  
    try:  
        cart_str = request.COOKIES.get('cart', '{}')  
        cart = json.loads(cart_str)  
    except json.JSONDecodeError:  
        cart = {}  

    cart_items = []  
    total_without_discount = Decimal('0.00')  
    total_discount = Decimal('0.00')  
    final_total = Decimal('0.00')  

    for pid, data in cart.items():  
        try:  
            product = Product.objects.get(id=int(pid))  
            qty = data.get('quantity', 1)  
            original_price = product.price  
            discounted_price = product.discount_price if hasattr(product, 'discount_price') and product.discount_price else original_price  

            item_original_total = original_price * qty  
            item_discount = (original_price - discounted_price) * qty if discounted_price < original_price else Decimal('0')  
            item_final_total = discounted_price * qty  

            total_without_discount += item_original_total  
            total_discount += item_discount  
            final_total += item_final_total  

            cart_items.append({  
                'product': product,  
                'quantity': qty,  
                'original_unit_price': original_price,  
                'unit_price': discounted_price,  
                'item_total': item_final_total,  
            })  
        except Product.DoesNotExist:  
            continue  

    context = {  
        'cart_items': cart_items,  
        'total_without_discount': total_without_discount,  
        'total_discount': total_discount,  
        'final_total': final_total,  
    }  
    return render(request, 'cart/cart.html', context)  