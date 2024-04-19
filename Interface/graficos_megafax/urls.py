
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.g_megafax ,name='g_megafax'),
    path('busqueda/',views.busqueda_m,name='busqueda_m')
]

#path('delete/', views.delete, name='delete'),