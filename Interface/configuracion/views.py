from django.shortcuts import render
from django.http import HttpResponse
from index.models import isdbt,megafax,log
from django.shortcuts import redirect
from django.contrib import messages
import re


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
    patron_ip = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'

    if request.method != 'POST':
        return HttpResponse("Metodo Invalido")

    IP = request.POST['IP']
    BR = request.POST['BR']
    nombre_canal= request.POST['nombre']
    origen = request.POST['origen']

    if nombre_canal == "":
        messages.error(request,'NO GUARDADO: Por favor, selecciona un origen y canal.')
        return redirect('config')
    

    if IP != "":
        if not re.match(patron_ip, IP):
            messages.error(request,'NO GUARDADO: Por favor, ingrese una IP válida.')
            return redirect('config')

        partes = IP.split('.')
        for parte in partes:
            if not 0 <= int(parte) <= 255:
                messages.error(request,'NO GUARDADO: Por favor, ingrese una IP válida.')
                return redirect('config')

        if origen == 'ISDBT':
            dato = isdbt.objects.get(nombre=nombre_canal)
            dato.ip=IP
            dato.save()
        else:
            dato = megafax.objects.get(nombre=nombre_canal)
            dato.ip=IP
            dato.save()
    

    if BR != "":
        try:
            float(BR)

        except:
            messages.error(request,'NO GUARDADO: Por favor, ingrese un BR minimo válido.')
            return redirect('config')
        
        if origen == 'ISDBT':
            dato = isdbt.objects.get(nombre=nombre_canal)
            dato.BR_min=BR
            dato.save()
        else:
            dato = megafax.objects.get(nombre=nombre_canal)
            dato.BR_min=BR
            dato.save()


    messages.error(request,'GUARDADO')
    return redirect('config')

def act_log(request):
    datos = log.objects.all().order_by('-id')
    return render(request,'config.html',{'log':datos})