from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm
from .models import Category, Product


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
                f"Registration successful. {request.user.username} are now logged in.",
            )
            return redirect("home") 
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




def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, "store/product_detail.html", {"product": product})


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(
        request,
        "store/category_products.html",
        {"category": category, "products": products},
    )
