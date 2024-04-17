
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index ,name='g_megafax')
]

#path('delete/', views.delete, name='delete'),