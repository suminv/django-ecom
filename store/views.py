from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .forms import SignUpForm
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
            messages.success(request, f"Registration successful. {request.user.username} are now logged in.")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("register")
    else:
        return render(request, "store/register.html", {"form": form})
    

def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, "store/product_detail.html", {"product": product})
