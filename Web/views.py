from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def product(request):
    return render(request, 'product.html')

def add_product(request):
    return render(request, 'add_product.html')

def about(request):
    return render(request, 'about.html')