from django.urls import path
from django.http import JsonResponse, HttpResponse

from .database import product


def get_products(request):
    result = product.get_products()
    return JsonResponse(result)



api = [
    path("get_products", get_products),
]