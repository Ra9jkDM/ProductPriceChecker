from django.urls import path
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound

import json

from ..database import product



def get_products(request):
    result = product.get_products()
    return JsonResponse(result)

def get_product(request):
    if request.method == "POST":
        print( request.FILES)

        json_data = b''
        for i in request.FILES["data"]:
            json_data += i

        json_data = json.loads(json_data)
        print(json_data, json_data["name"])

        file = request.FILES['image']
        # print((str(file)+"..dfwef.wef.wef.wef.wef.662.gif").split(".")[-1])
        # with open(f"Web/upload/products/14.jpg", "wb+") as f:
        #     for chunk in file.chunks():
        #         f.write(chunk)

        product.save_product(json_data, file)
        

        return JsonResponse({"status": "ok"})
    else:
        id = request.GET.get("id")
        result = product.get_product(id)
        return JsonResponse(result)




api = [
    path("products", get_products),
    path("product", get_product),
]