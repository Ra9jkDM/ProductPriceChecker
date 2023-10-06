from django.urls import path
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound

import json

from ..database import product



def get_products(request):
    result = product.get_products()
    return JsonResponse(result)

def _get_json_data(bytes_data):
    json_data = b''
    for i in bytes_data:
        json_data += i
    
    return json_data

def get_product(request):
    if request.method == "POST":
        json_data = _get_json_data(request.FILES["data"])
        json_data = json.loads(json_data)

        if request.FILES.get('image'):
            file = request.FILES['image']
        else:
            return JsonResponse({"status": "error"})

        result = product.save_product(json_data, file)
        
        return JsonResponse(result)
    else:
        id = request.GET.get("id")
        result = product.get_product(id)
        return JsonResponse(result)




api = [
    path("products", get_products),
    path("product", get_product),
]