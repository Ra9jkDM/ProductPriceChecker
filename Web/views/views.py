from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

from ..database import shops  

IMAGE_PATH = "Web/upload"

def index(request):
    return render(request, 'index.html')

def product(request):
    id = request.GET.get("id")

    response = render(request, 'product.html')
    response.set_cookie('id', id, max_age=30)
    return response

def add_product(request):
    data = shops.get_shops()
    return render(request, 'add_product.html', context={"shops": data})

def about(request):
    return render(request, 'about.html')

def images(request, path, name):
    try:
        image_data = open(f"{IMAGE_PATH}/{path}/{name}", "rb").read()
        return HttpResponse(image_data)
    except:
        return HttpResponseNotFound()