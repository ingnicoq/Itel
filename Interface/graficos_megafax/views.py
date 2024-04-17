from django.shortcuts import render
from django.http import HttpResponse
from .models import BR

"""
def delete(request): 
    dato = BR.objects.all()
    dato.delete()
    #isdbt.objects.filter(nombre='ItelTV').delete()
    return HttpResponse('Borrado') 
"""

def index(request): 
    
    #isdbt.objects.filter(nombre='ItelTV').delete()
    return render(request,'graf_megafax.html',{})