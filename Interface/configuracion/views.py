from django.shortcuts import render
from django.http import HttpResponse
from index.models import isdbt,megafax
from django.shortcuts import redirect

def config(request): 
    datos = isdbt.objects.all().order_by('nombre')
    dicc ={}
    for elementos in datos:
        dicc[elementos.nombre]=elementos.nombre.replace(" ","_")
    
    datos2 = megafax.objects.all().order_by('nombre')
    dicc2 ={}
    for elementos in datos2:
        dicc2[elementos.nombre]=elementos.nombre.replace(" ","_")

    return render(request,'config.html',{'datos':dicc,'datos2':dicc2,})

def actualizacion(request):
    if request.method != 'POST':
        return HttpResponse("Metodo Invalido")

    IP = request.POST['IP']
    BR = request.POST['BR']
    nombre= request.POST['nombre']
    origen = request.POST['origen']

    if nombre == "":
        return HttpResponse("Seleccionar Origen y Canal")

    print(IP)
    print(BR)
    print(nombre)
    print(origen)

    return redirect('config')