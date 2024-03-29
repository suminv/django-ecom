from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from store.models import Product

from .cart import Cart


def cart_summary(request):
    return render(request, "cart/cart_summary.html")


def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # test for POST
    if request.POST.get("action") == "post":
        # Get stuff
        product_id = int(request.POST.get("product_id"))

        # lookup product in DB
        product = get_object_or_404(Product, id=product_id)

        # Save to session
        cart.add(product=product)

        # Return resonse
        response = JsonResponse({"Product Name: ": product.name})

        messages.success(request, ("Product Added To Cart..."))
        return response


def cart_delete(request):
    return render(request, "cart/cart_delete.html")


def cart_update(request):
    return render(request, "cart/cart_update.html")
