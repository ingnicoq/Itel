from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request,'index.html',{})

def principal(request, name):

    categoria = ['code','design','admin']

    return render(request,'principal.html',{'nombre':name , 'categ':categoria}) #parametros de render (requestr, dir del template, parametros que le paso)

def secundaria(request):
    return render(request,'secundaria.html',{})


def tercera(request):
    return render(request,'tercera.html',{})