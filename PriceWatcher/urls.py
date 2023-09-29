"""
URL configuration for PriceWatcher project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from Web.views.views import index, product, add_product, about, images
from Web.views.api import api
from Web.views.proxy import proxy

urlpatterns = [
    path('', index),
    path('product/', product),
    path('add_product/', add_product),
    path('about/', about),

    path('img/<str:path>/<str:name>', images),

    path("api/", include(api)),
    path("proxy/", include(proxy)),

    path('admin/', admin.site.urls),
]

# sass -w sass/styles.scss css/styles.css
# export $(cat .env)
# python manage.py runserver