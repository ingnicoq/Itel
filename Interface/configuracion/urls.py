
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.config ,name='config'),
    path('actualizacion/',views.actualizacion ,name='actualizacion'),
    path('logs/',views.act_log,name='act_log')
]
#path('delete/', views.delete, name='delete'),