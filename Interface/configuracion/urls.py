
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.config ,name='config')
]
#path('delete/', views.delete, name='delete'),