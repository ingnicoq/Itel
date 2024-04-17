from django.shortcuts import render
from django.http import HttpResponse


def config(request): 
    return render(request,'config.html',{})