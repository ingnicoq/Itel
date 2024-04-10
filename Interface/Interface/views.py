from django.http import HttpResponse
from django.shortcuts import render

def principal(request, name):

    categoria = ['code','design','admin']

    return render(request,'principal.html',{'nombre':name , 'categ':categoria}) #parametros de render (requestr, dir del template, parametros que le paso)

