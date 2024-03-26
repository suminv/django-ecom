from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .models import Product


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
