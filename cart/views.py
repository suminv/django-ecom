from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from store.models import Product

from .cart import Cart


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    return render(
        request,
        "cart/cart_summary.html",
        {"cart_products": cart_products, "quantities": quantities},
    )


def cart_add(request):
    # Get the cart
    cart = Cart(request)

    # Test for POST
    if request.POST.get("action") == "post":
        # Get product ID from the request
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))
        # Lookup product in DB
        product = get_object_or_404(Product, id=product_id)

        # Save product to cart
        cart.add(product=product, quantity=product_qty)

        # Get updated cart quantity
        cart_quantity = cart.__len__()

        # Return JSON response with updated cart quantity
        messages.success(request, f"{product.name} was added to your cart!")
        response_data = {"cart_quantity": cart_quantity}
        return JsonResponse(response_data)

    # Return error response if the request method is not POST or 'action' parameter is not set
    return JsonResponse({"error": "Invalid request"}, status=400)


def cart_delete(request):
    return render(request, "cart/cart_delete.html")


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty':product_qty})
        #return redirect('cart_summary')
        messages.success(request, ("Your Cart Has Been Updated..."))
        return response