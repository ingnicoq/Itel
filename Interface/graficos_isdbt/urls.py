
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.g_isdbt ,name='g_isdbt')
]
#path('delete/', views.delete, name='delete'),