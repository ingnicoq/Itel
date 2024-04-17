"""
URL configuration for Interface project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name='index'),
    path('graf_isdbt/', views.graf_isdbt, name='graf_isdbt'),  
    path('graf_megafax/', views.graf_megafax, name='graf_megafax'),
    path('config/', views.config, name='config'),
    path('principal/',include('index.urls')),
    path('graph_isdbt/',include('graficos_isdbt.urls')),
    path('graph_megafax/',include('graficos_megafax.urls'))
]
