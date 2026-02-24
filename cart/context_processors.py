import json  

def cart_count(request):  
    try:  
        cart_str = request.COOKIES.get('cart', '{}')  
        cart = json.loads(cart_str)  
        count = sum(item.get('quantity', 0) for item in cart.values())  
    except json.JSONDecodeError:  
        count = 0  
    return {'cart_count': count}  