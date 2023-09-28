from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

def index(request):
    return render(request, 'index.html')

def product(request):
    return render(request, 'product.html')

def add_product(request):
    return render(request, 'add_product.html')

def about(request):
    return render(request, 'about.html')

def images(request, path, name):
    try:
        image_data = open(f"Web/upload/{path}/{name}", "rb").read()
        return HttpResponse(image_data)
    except:
        return HttpResponseNotFound()