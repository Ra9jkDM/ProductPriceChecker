from django.urls import path
from django.http import JsonResponse, HttpResponse

from .database import product


def get_products(request):
    result = product.get_products()
    return JsonResponse(result)

def get_product(request):
    id = request.GET.get("id")
    result = product.get_product(id)
    return JsonResponse(result)

api = [
    path("products", get_products),
    path("product", get_product)
]