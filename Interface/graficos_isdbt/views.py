from django.shortcuts import render
from django.http import HttpResponse
from .models import BR
from index.models import isdbt
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def g_isdbt(request): 

    datos = isdbt.objects.all().order_by('nombre')
    dicc ={}
    for elementos in datos:
        dicc[elementos.nombre]=elementos.nombre.replace(" ","_")
    
    return render(request,'graf_isdbt.html',{'datos':dicc})

def busqueda(request):

    canal_seleccionado = request.GET.get('canal')
    canal_seleccionado = canal_seleccionado.replace("_"," ")
    
    id_canal = isdbt.objects.get(nombre=canal_seleccionado)
    cons=id_canal.BR_min

    result = BR.objects.filter(canal_id=id_canal.canal_id).order_by('id')

    ultimo_registro = BR.objects.filter(canal_id=id_canal.canal_id).order_by('id').last()

    ulitma_fecha=datetime(int(ultimo_registro.year),int(ultimo_registro.month),int(ultimo_registro.day),int(ultimo_registro.hour),int(ultimo_registro.min),int(ultimo_registro.sec))


    fecha_7dias= ulitma_fecha - timedelta(days=7)

    fecha_1dia = ulitma_fecha - timedelta(days=1)

    fecha_6horas = ulitma_fecha - timedelta(hours=6)
    
    fecha_1hora = ulitma_fecha - timedelta(hours=1)

    dicc7d={}
    dicc1d={}
    dicc6h={}
    dicc1h={}

    for elemento in result:
        time=datetime(int(elemento.year),int(elemento.month),int(elemento.day),int(elemento.hour),int(elemento.min),int(elemento.sec))
        
        if time >= fecha_7dias:
            time_str=time.strftime('%Y-%m-%d %H:%M:%S')
            dicc7d[time_str]=[elemento.BR,cons]
        if time >= fecha_1dia:
            time_str=time.strftime('%Y-%m-%d %H:%M:%S')
            dicc1d[time_str]=[elemento.BR,cons]
        if time >= fecha_6horas:
            time_str=time.strftime('%Y-%m-%d %H:%M:%S')
            dicc6h[time_str]=[elemento.BR,cons]
        if time >= fecha_1hora:
            time_str=time.strftime('%Y-%m-%d %H:%M:%S')
            dicc1h[time_str]=[elemento.BR,cons]

    br7d=[]
    time7d=[]
    cons7d=[]
    for key,value in dicc7d.items():
        br7d.append(float(value[0]))
        cons7d.append(float(value[1]))
        sub_fecha= key[5:10]
        time7d.append(sub_fecha)

    br1d=[]
    time1d=[]
    cons1d=[]
    for key,value in dicc1d.items():
        br1d.append(float(value[0]))
        cons1d.append(float(value[1]))
        sub_fecha= key[5:13]
        time1d.append(sub_fecha)

    br6h=[]
    time6h=[]
    cons6h=[]
    for key,value in dicc6h.items():
        br6h.append(float(value[0]))
        cons6h.append(float(value[1]))
        sub_fecha= key[11:16]
        time6h.append(sub_fecha) 

    br1h=[]
    time1h=[]
    cons1h=[]
    for key,value in dicc1h.items():
        br1h.append(float(value[0]))
        cons1h.append(float(value[1]))
        sub_fecha= key[5:13]
        time1h.append(sub_fecha)  
    


    # Aquí puedes realizar tu búsqueda en la base de datos utilizando el valor recibido
    #datos = isdbt.objects.get(nombre=canal_seleccionado)
    # Supongamos que tienes una lista de resultados que deseas devolver
    #resultados = BR.objects.filter(canal_id=datos.canal_id)

    # Renderiza una plantilla parcial para mostrar los resultados
    return render(request, 'busqueda.html', {'br7d':br7d,'time7d':time7d,'cons7d':cons7d,'br1d':br1d,'time1d':time1d,'cons1d':cons1d,'br6h':br6h,'time6h':time6h,'cons6h':cons6h,'br1h':br1h,'time1h':time1h,'cons1h':cons1h})

"""
def delete(request): 
    dato = BR.objects.all()
    dato.delete()
    #isdbt.objects.filter(nombre='ItelTV').delete()
    return HttpResponse('Borrado') 
"""