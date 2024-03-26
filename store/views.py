from django.shortcuts import render
from .models import Product


def home(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', {'products': products})

def about(request):
    return render(request, 'store/about.html')