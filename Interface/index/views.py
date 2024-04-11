from django.shortcuts import render
from django.http import HttpResponse
from .models import isdbt

# Create your views here.

def test (request):
    return HttpResponse('Funciona correcto')

def create (request):
    datos = isdbt(nombre='ItelTV',ip='223.2.2.2',BR_min=2,canal_id='canal_1',estado=1)
    datos.save()
    #datos = isdbt.objects.acreate(nombre='ItelTV',ip='223.2.2.2',BR_min=2,canal_id='canal_1',estado=1)
    return HttpResponse('CREATE')

def delete(request): 
    dato = isdbt.objects.get(nombre='ItelTV')
    dato.delete()
    #isdbt.objects.filter(nombre='ItelTV').delete()
    return HttpResponse('Borrado') 

def query(request):
    #obtener todos los elementos
    datos = isdbt.objects.all().order_by('nombre') #ordenamiento por nombre - no es necesario-

    #obtener los datos por condicion
    datos_filtrados=isdbt.objects.filter(id=20) #filter(id__lte= 20) ---->       __lte(menor o igual) __gte(mayor o igual) __lt __gt (menor que , mayor que) __contains __exact 

    #obtener un unico objeto
    unico = isdbt.objects.get(id=50)

    #obtener elementos con limites
    limite= isdbt.objects.all()[:10] #[offset:limit]


    return render(request,'index.html',{'datos':datos,'datos_filtrados':datos_filtrados,'unico':unico,'limite':limite})

def actualiz(request):

    dato = isdbt.objects.get(id=10)
    dato.nombre='pepe'

    dato.save()
    return HttpResponse('Actualizado')