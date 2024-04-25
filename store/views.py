import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count

from .forms import ChangePasswordForm, ReviewForm, SignUpForm, UpdateUserForm, UserInfoForm
from .models import Category, Product, Profile, Review
from payment.models import ShipppingAddres
from payment.forms import ShippingForm


from cart.cart import Cart

def home(request):
    products = Product.objects.all()
    return render(request, "store/index.html", {"products": products})


def about(request):
    return render(request, "store/about.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Do some shoping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            # Get their saves cart from database
            saved_cart = current_user.old_cart
            # Convert database string to python dictionary
            if saved_cart:
                # convert to dict usint json.loads
                convert_data = json.loads(saved_cart)
                # add the loaded cart dictionary to session
                cart = Cart(request)
                # Loop thru the cart and add the items from the database
                for key, value in convert_data.items():
                    cart.db_add(product=key, quantity=value)


            messages.success(request, "Login Successfully")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")
    else:
        return render(request, "store/login.html")


def logout_user(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect("home")


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request,
                f"Registration successful. {request.user.username} are now logged in. Please update your information.",
            )
            return redirect("update_info")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("register")
    else:
        return render(request, "store/register.html", {"form": form})


def update_user(request):
    if request.user.is_authenticated:
        # Get the current user
        current_user = User.objects.get(id=request.user.id)
        # Check if the POST request and fill data in current_user_form to update
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, "Profile updated successfully")
            return redirect("home")
        return render(request, "store/update_user.html", {"user_form": user_form})
    else:
        messages.error(request, "You must be logged in to view this page")
        return redirect("home")


def update_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password updated successfully")
            login(request, request.user)
            return redirect("update_user")
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = ChangePasswordForm(request.user)
    return render(request, "store/update_password.html", {"form": form})


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        shipping_user = ShipppingAddres.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, "You information updated successfully")
            return redirect("home")
        return render(request, "store/update_info.html", {"form": form, "shipping_form": shipping_form})
    else:
        messages.error(request, "You must be logged in to view this page")
        return redirect("home")


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    review = Review.objects.filter(product=product)
    total_review = review.count()
    average_rating = review.aggregate(Avg("rating"))["rating__avg"]
    my_range = range(1, 6)
    # average_star = '*' * int(average_rating)
    return render(request, "store/product_detail.html", {"product": product, "review": review, "total_review": total_review, "average_rating": average_rating, "my_range": my_range})



def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(
        request,
        "store/category_products.html",
        {"category": category, "products": products},
    )


def search(request):
    # Determine if they filled out the form
    if request.method == "POST":
        searched = request.POST["searched"]
        # get sql search in Product table by name
        searched = Product.objects.filter(
            Q(name__icontains=searched) | Q(description__icontains=searched)
        )
        # Check for null
        if not searched:
            messages.error(request, "No products found")
            return render(request, "store/search.html", {})
        else:
            return render(request, "store/search.html", {"searched": searched})
    else:
        return render(request, "store/search.html", {})

@login_required
def add_review(request, slug):
    """
    Adds a review for a product.

    Parameters:
        request (HttpRequest): The HTTP request object.
        slug (str): The slug of the product.

    Returns:
        HttpResponse: The response object.
    """
    product = get_object_or_404(Product, slug=slug)
    
    if request.method =='POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Review added successfully")
            return redirect('product_detail', slug=slug)
    else:
        form = ReviewForm() 
    return render(request, 'store/add_review.html', {'form': form, 'product': product})



def all_reviews(request, slug):
    """
    Retrieves all reviews for a given product and renders them in the 'store/all_reviews.html' template.
    
    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The slug of the product.
        
    Returns:
        HttpResponse: The rendered 'store/all_reviews.html' template with the reviews and product information.
    """
    product = get_object_or_404(Product, slug=slug)
    reviews = Review.objects.filter(product=product).order_by('-data_time_stamp')
    if reviews:
        return render(request, 'store/all_reviews.html', {'reviews': reviews, 'product': product})
    else:
        messages.error(request, "No reviews found") 
        return redirect('home')
    
    