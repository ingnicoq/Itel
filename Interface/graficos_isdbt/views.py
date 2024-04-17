from django.shortcuts import render
from django.http import HttpResponse
from .models import BR

def g_isdbt(request): 
    return render(request,'graf_isdbt.html',{})

"""
def delete(request): 
    dato = BR.objects.all()
    dato.delete()
    #isdbt.objects.filter(nombre='ItelTV').delete()
    return HttpResponse('Borrado') 
"""