from .cart import Cart

def get_cart(request):
    return {"cart": Cart(request)}
