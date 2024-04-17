from django.http import HttpResponse
from django.shortcuts import render



def graf_isdbt(request,name):

    categoria = ['code','design','admin']

    return render(request,'graf_isdbt.html',{'nombre':name , 'categ':categoria}) #parametros de render (requestr, dir del template, parametros que le paso)

   # def graf_isdbt(request):

    #return render(request,'graf_isdbt.html',{}) 

def index(request):
    return render(request,'index.html',{})

def graf_megafax(request):
    return render(request,'graf_megafax.html',{})


def config(request):
    return render(request,'config.html',{})

