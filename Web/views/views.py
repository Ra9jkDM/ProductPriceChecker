from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

from ..database import shops  

from ..S3 import main as s3


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

def _s3_get_files(path):
    try:
        file = s3.get_object(path)
        return HttpResponse(file)
    except:
        return HttpResponseNotFound()

def fonts(request, name):
    return _s3_get_files(f"fonts/{name}")

def images(request, name):
    return _s3_get_files(f"img/{name}")

def upload_images(request, path, name):
    return _s3_get_files(f"upload/{path}/{name}")

# TODO return fonts from S#/MinIO and change upload dir + add 'test_files' dir to .gitignore
# then delete 'upload/products' and 'static/img' and 'static/fonts'
# Shedued task

