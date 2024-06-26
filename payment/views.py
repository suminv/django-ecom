from django.shortcuts import render, redirect
from django.utils import timezone
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShipppingAddres, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product, Profile

from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.contrib import messages
from .models import Order, OrderItem

def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = get_object_or_404(Order, id=pk)
        order_items = OrderItem.objects.filter(order=pk)

        if request.method == 'POST':
            status = request.POST.get('shipping_status')
            now = timezone.now()

            if status == 'True':
                order.shipped = True
                order.date_shipped = now
                order.save()
                messages.success(request, 'Order marked as shipped')
            else:
                order.shipped = False
                order.date_shipped = None  # Optionally reset the date shipped
                order.save()
                messages.success(request, 'Order marked as not shipped')
            
            return redirect('home')

        return render(request, "payment/orders.html", {'order': order, 'order_items': order_items})

    else:
        messages.error(request, 'Access Denied.')
        return redirect('home')



def shipping_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        # Проверяем значение переключателя
        show_shipping = request.GET.get('show_shipping')

        if show_shipping == 'true':
            orders = Order.objects.filter(shipped=True)
            messages.success(request, 'Choiced Orders Shipped')
        elif show_shipping == 'false':
            orders = Order.objects.filter(shipped=False)
            messages.success(request, 'Choiced Orders Not Shipped')
        else:
            orders = []  # Инициализируем пустой список для заказов

        return render(request, "payment/shipping_dashboard.html", {'orders': orders})
    else:
        messages.success(request, 'Access Denied.')
        return redirect('home')


def payment_success(request):
    return render(request, "payment/payment_success.html", {})


def checkout(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.get_totals()

    if request.user.is_authenticated:
        # Checkout as logged in user
        # Shipping User
        shipping_user = ShipppingAddres.objects.get(user__id=request.user.id)
        # Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(
            request,
            "payment/checkout.html",
            {
                "cart_products": cart_products,
                "quantities": quantities,
                "totals": totals,
                "shipping_form": shipping_form,
            },
        )
    else:
        # Checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(
            request,
            "payment/checkout.html",
            {
                "cart_products": cart_products,
                "quantities": quantities,
                "totals": totals,
                "shipping_form": shipping_form,
            },
        )


def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.get_totals()

        # Create a session with Shipping Info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping


        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_info": request.POST, "billing_form": billing_form})
            
        else:
            billing_form = PaymentForm()
           
            return render(request, "payment/billing_info.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_info": request.POST, "billing_form": billing_form})

        # shipping_form = request.POST
        # return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})

    else:
        messages.success(request, 'Access Denied.')
        return redirect('home')



def process_order(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.get_totals()

        # Get Billing Info from the last page
        payment_form = PaymentForm(request.POST or None)
        # Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')

        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']


        # Create Shipping Address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"

        amount_paid = totals

        # Create Order
        if request.user.is_authenticated:
            user = request.user
            create_order = Order.objects.create(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Add order items
            # Get order id
            order_id = create_order.pk
            # Get product info
            for product in cart_products():
                # Get product id
                product_id = product.id
                # Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                # Get product quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quatity=value, price=price)
                        create_order_item.save()

                # Empty cart
            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]
            # Delete Cart from Database (old_cart field)
            current_user = Profile.objects.filter(user__id=request.user.id)
            # Delete shopping cart in database (old_cart field)
            current_user.update(old_cart="")


            messages.success(request, 'Order Placed Successfully')
            return redirect('home')
        else:
            create_order = Order.objects.create(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            order_id = create_order.pk
            # Get product info
            for product in cart_products():
                # Get product id
                product_id = product.id
                # Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                # Get product quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quatity=value, price=price)
                        create_order_item.save()
            # Empty cart
            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]

            messages.success(request, 'Order Placed Successfully')
            return redirect('home')

    else:
        messages.success(request, 'Access Denied.')
        return redirect('home')



