from django.shortcuts import render
from django.http import HttpResponse
from .models import isdbt,megafax,log
from django.template.loader import render_to_string
from graficos_isdbt.models import BR as BR_ISDBT
from graficos_megafax.models import BR as BR_MEGA

# Create your views here.



def query(request):
    #obtener todos los elementos
    datos = isdbt.objects.all().order_by('-estado','nombre') #ordenamiento por nombre - no es necesario-
    
    datos2=[]
    i=0
    for items in datos:
        result = BR_ISDBT.objects.filter(canal_id = items.canal_id).order_by('-id')[:1]
        for elementos in result:
            br_vivo = elementos.BR
        datos2.append({'nombre':items.nombre,'ip':items.ip,'br_min':items.BR_min,'br_vivo':br_vivo,'estado':items.estado})
        i+=1

    #obtener los datos por condicion
    #datos_filtrados=isdbt.objects.filter(id=20) #filter(id__lte= 20) ---->       __lte(menor o igual) __gte(mayor o igual) __lt __gt (menor que , mayor que) __contains __exact 

    #obtener un unico objeto
    #unico = isdbt.objects.get(id=50)

    #obtener elementos con limites
    #limite= isdbt.objects.all()[:10] #[offset:limit]

    datos1 = megafax.objects.all().order_by('-estado','nombre')
    datos3=[]
    i=0
    for items in datos1:
        result = BR_MEGA.objects.filter(canal_id = items.canal_id).order_by('-id')[:1]
        for elementos in result:
            br_vivo = elementos.BR
        datos3.append({'nombre':items.nombre,'ip':items.ip,'br_min':items.BR_min,'br_vivo':br_vivo,'estado':items.estado})
        i+=1

    return render(request,'index.html',{'datos2':datos2,'datos1':datos3}) #,'datos_filtrados':datos_filtrados,'unico':unico,'limite':limite})

"""
def test (request):
    return HttpResponse('Funciona correcto')

def create (request):
    #datos = isdbt(nombre='ItelTV',ip='223.2.2.2',BR_min=2,canal_id='canal_1',estado=1)
    #datos.save()
    #datos = isdbt.objects.acreate(nombre='ItelTV',ip='223.2.2.2',BR_min=2,canal_id='canal_1',estado=1)
    
    
    datos_1=isdbt(nombre='ITELTV HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_1',estado=0)
    datos_2=isdbt(nombre='AMERICA HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_2',estado=0)
    datos_3=isdbt(nombre='TV PUBLICA HD',ip='237.2.2.3',BR_min=5.1,canal_id='canal_3',estado=1)
    datos_4=isdbt(nombre='CANAL 9 HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_4',estado=0)
    datos_5=isdbt(nombre='TELEFE HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_5',estado=0)
    datos_6=isdbt(nombre='EL TRECE HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_6',estado=0)
    datos_7=isdbt(nombre='T5 SATELITAL HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_7',estado=0)
    datos_8=isdbt(nombre='TN HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_8',estado=0)
    datos_9=isdbt(nombre='A24 HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_9',estado=0)
    datos_10=isdbt(nombre='CANAL 26',ip='237.2.2.10',BR_min=1.1,canal_id='canal_10',estado=1)
    datos_11=isdbt(nombre='C5N',ip='237.2.2.11',BR_min=1.1,canal_id='canal_11',estado=0)
    datos_12=isdbt(nombre='CRONICA TV',ip='237.2.2.12',BR_min=1.1,canal_id='canal_12',estado=0)
    datos_13=isdbt(nombre='LN+',ip='237.2.2.13',BR_min=1.1,canal_id='canal_13',estado=0)
    datos_14=isdbt(nombre='RURAL',ip='237.2.2.14',BR_min=1.6,canal_id='canal_14',estado=0)
    datos_15=isdbt(nombre='TyC SPORTS HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_15',estado=0)
    datos_16=isdbt(nombre='FOX SPORTS',ip='237.2.2.16',BR_min=3.2,canal_id='canal_16',estado=0)
    datos_17=isdbt(nombre='FOX SPORTS 2',ip='0.0.0.0',BR_min=0.5,canal_id='canal_17',estado=0)
    datos_18=isdbt(nombre='FOX SPORTS 3',ip='0.0.0.0',BR_min=0.5,canal_id='canal_18',estado=0)
    datos_19=isdbt(nombre='ESPN',ip='237.2.2.19',BR_min=3,canal_id='canal_19',estado=0)
    datos_20=isdbt(nombre='ESPN 2',ip='0.0.0.0',BR_min=0.5,canal_id='canal_20',estado=0)
    datos_21=isdbt(nombre='ESPN 3',ip='0.0.0.0',BR_min=0.5,canal_id='canal_21',estado=1)
    datos_22=isdbt(nombre='ESPN 4',ip='0.0.0.0',BR_min=0.5,canal_id='canal_22',estado=0)
    datos_23=isdbt(nombre='DEPORTV HD',ip='237.2.2.23',BR_min=1.6,canal_id='canal_23',estado=0)
    datos_24=isdbt(nombre='AMERICA SPORTS',ip='237.2.2.24',BR_min=1.7,canal_id='canal_24',estado=0)
    datos_25=isdbt(nombre='DISCOVERY KIDS',ip='237.2.2.25',BR_min=1.2,canal_id='canal_25',estado=0)
    datos_26=isdbt(nombre='CARTOON NETWORK',ip='237.2.2.26',BR_min=1,canal_id='canal_26',estado=0)
    datos_27=isdbt(nombre='DISNEY',ip='0.0.0.0',BR_min=0.5,canal_id='canal_27',estado=0)
    datos_28=isdbt(nombre='NICKELODEON',ip='237.2.2.28',BR_min=1.2,canal_id='canal_28',estado=0)
    datos_29=isdbt(nombre='DISNEY JUNIOR',ip='0.0.0.0',BR_min=0.5,canal_id='canal_29',estado=0)
    datos_30=isdbt(nombre='CARTOONITO',ip='0.0.0.0',BR_min=0.5,canal_id='canal_30',estado=1)
    datos_31=isdbt(nombre='NICK JR',ip='237.2.2.31',BR_min=1.2,canal_id='canal_31',estado=0)
    datos_32=isdbt(nombre='PAKA PAKA',ip='237.2.2.32',BR_min=1.2,canal_id='canal_32',estado=0)
    datos_33=isdbt(nombre='TNT HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_33',estado=0)
    datos_34=isdbt(nombre='WB',ip='237.2.2.34',BR_min=2,canal_id='canal_34',estado=0)
    datos_35=isdbt(nombre='SONY HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_35',estado=0)
    datos_36=isdbt(nombre='SPACE HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_36',estado=0)
    datos_37=isdbt(nombre='A&E HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_37',estado=1)
    datos_38=isdbt(nombre='AXN HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_38',estado=0)
    datos_39=isdbt(nombre='CINECANAL HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_39',estado=0)
    datos_40=isdbt(nombre='STAR HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_40',estado=0)
    datos_41=isdbt(nombre='DE PELICULAS',ip='0.0.0.0',BR_min=0.5,canal_id='canal_41',estado=0)
    datos_42=isdbt(nombre='TELEMUNDO HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_42',estado=1)
    datos_43=isdbt(nombre='FX HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_43',estado=0)
    datos_44=isdbt(nombre='STUDIO UNIVERSAL',ip='0.0.0.0',BR_min=0.5,canal_id='canal_44',estado=0)
    datos_45=isdbt(nombre='UNIVERSAL',ip='0.0.0.0',BR_min=0.5,canal_id='canal_45',estado=1)
    datos_46=isdbt(nombre='USA',ip='0.0.0.0',BR_min=0.5,canal_id='canal_46',estado=0)
    datos_47=isdbt(nombre='PARMOUNT HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_47',estado=1)
    datos_48=isdbt(nombre='CINEAR',ip='237.2.2.49',BR_min=1.6,canal_id='canal_48',estado=0)
    datos_49=isdbt(nombre='EUROPA HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_49',estado=0)
    datos_50=isdbt(nombre='AMC HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_50',estado=0)
    datos_51=isdbt(nombre='CINEMAX',ip='0.0.0.0',BR_min=0.5,canal_id='canal_51',estado=0)
    datos_52=isdbt(nombre='TNT NOVELAS',ip='237.2.2.38',BR_min=2.7,canal_id='canal_52',estado=0)
    datos_53=isdbt(nombre='TCM',ip='0.0.0.0',BR_min=0.5,canal_id='canal_53',estado=0)
    datos_54=isdbt(nombre='VOLVER',ip='237.2.2.55',BR_min=3.3,canal_id='canal_54',estado=0)
    datos_55=isdbt(nombre='GOLDEN HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_55',estado=0)
    datos_56=isdbt(nombre='E! HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_56',estado=0)
    datos_57=isdbt(nombre='TURBO HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_57',estado=0)
    datos_58=isdbt(nombre='HOME & HEALTH HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_58',estado=0)
    datos_59=isdbt(nombre='GARAGE TV',ip='0.0.0.0',BR_min=0.5,canal_id='canal_59',estado=0)
    datos_60=isdbt(nombre='LIFETIME HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_60',estado=0)
    datos_61=isdbt(nombre='ADULT SWIM',ip='0.0.0.0',BR_min=0.5,canal_id='canal_61',estado=0)
    datos_62=isdbt(nombre='FOOD NETWORK HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_62',estado=1)
    datos_63=isdbt(nombre='TLC HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_63',estado=0)
    datos_64=isdbt(nombre='LAS ESTRELLAS HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_64',estado=0)
    datos_65=isdbt(nombre='FILM & ARTS HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_65',estado=0)
    datos_66=isdbt(nombre='EL GOURMET HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_66',estado=0)
    datos_67=isdbt(nombre='MAS CHIC',ip='0.0.0.0',BR_min=0.5,canal_id='canal_67',estado=0)
    datos_68=isdbt(nombre='CANAL A',ip='237.2.2.69',BR_min=1.7,canal_id='canal_68',estado=0)
    datos_69=isdbt(nombre='METRO',ip='237.2.2.70',BR_min=1.7,canal_id='canal_69',estado=0)
    datos_70=isdbt(nombre='MAGAZINE',ip='237.2.2.71',BR_min=2.2,canal_id='canal_70',estado=0)
    datos_71=isdbt(nombre='ENCUENTRO HD',ip='237.2.2.72',BR_min=1.7,canal_id='canal_71',estado=0)
    datos_72=isdbt(nombre='TEC TV',ip='237.2.2.73',BR_min=1.1,canal_id='canal_72',estado=0)
    datos_73=isdbt(nombre='CONSTRUIR TV',ip='237.2.2.74',BR_min=1.6,canal_id='canal_73',estado=0)
    datos_74=isdbt(nombre='ARGENTINISIMA',ip='0.0.0.0',BR_min=0.5,canal_id='canal_74',estado=0)
    datos_75=isdbt(nombre='HGLA HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_75',estado=0)
    datos_76=isdbt(nombre='SCIENCE HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_76',estado=0)
    datos_77=isdbt(nombre='DISCOVERY HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_77',estado=0)
    datos_78=isdbt(nombre='WORLD HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_78',estado=0)
    datos_79=isdbt(nombre='THEATER HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_79',estado=0)
    datos_80=isdbt(nombre='HISTORY HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_80',estado=0)
    datos_81=isdbt(nombre='HISTORY2 HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_81',estado=0)
    datos_82=isdbt(nombre='NATGEO HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_82',estado=0)
    datos_83=isdbt(nombre='LOVE NATURE',ip='237.2.2.84',BR_min=2,canal_id='canal_83',estado=0)
    datos_84=isdbt(nombre='ID HD',ip='0.0.0.0',BR_min=0.5,canal_id='canal_84',estado=0)
    datos_85=isdbt(nombre='ANIMAL PLANET HD',ip='237.2.2.86',BR_min=2.5,canal_id='canal_85',estado=0)
    datos_86=isdbt(nombre='HTV',ip='0.0.0.0',BR_min=0.5,canal_id='canal_86',estado=0)
    datos_87=isdbt(nombre='MTV',ip='237.2.2.88',BR_min=2,canal_id='canal_87',estado=0)
    datos_88=isdbt(nombre='QUIERO',ip='237.2.2.89',BR_min=2.5,canal_id='canal_88',estado=0)
    datos_89=isdbt(nombre='CM',ip='237.2.2.90',BR_min=3,canal_id='canal_89',estado=0)
    datos_90=isdbt(nombre='MTV 80',ip='0.0.0.0',BR_min=0.5,canal_id='canal_90',estado=0)
    datos_91=isdbt(nombre='NUEVO TIEMPO',ip='237.2.2.92',BR_min=2,canal_id='canal_91',estado=0)
    datos_92=isdbt(nombre='EWTN',ip='237.2.2.93',BR_min=3,canal_id='canal_92',estado=0)
    datos_93=isdbt(nombre='ENLACE',ip='237.2.2.94',BR_min=1.5,canal_id='canal_93',estado=0)
    datos_94=isdbt(nombre='UNIFE',ip='237.2.2.95',BR_min=1.5,canal_id='canal_94',estado=0)
    datos_95=isdbt(nombre='CANAL LUZ',ip='237.2.2.96',BR_min=1.5,canal_id='canal_95',estado=0)

    datos_1.save()
    datos_2.save()
    datos_3.save()
    datos_4.save()
    datos_5.save()
    datos_6.save()
    datos_7.save()
    datos_8.save()
    datos_9.save()
    datos_10.save()
    datos_11.save()
    datos_12.save()
    datos_13.save()
    datos_14.save()
    datos_15.save()
    datos_16.save()
    datos_17.save()
    datos_18.save()
    datos_19.save()
    datos_20.save()
    datos_21.save()
    datos_22.save()
    datos_23.save()
    datos_24.save()
    datos_25.save()
    datos_26.save()
    datos_27.save()
    datos_28.save()
    datos_29.save()
    datos_30.save()
    datos_31.save()
    datos_32.save()
    datos_33.save()
    datos_34.save()
    datos_35.save()
    datos_36.save()
    datos_37.save()
    datos_38.save()
    datos_39.save()
    datos_40.save()
    datos_41.save()
    datos_42.save()
    datos_43.save()
    datos_44.save()
    datos_45.save()
    datos_46.save()
    datos_47.save()
    datos_48.save()
    datos_49.save()
    datos_50.save()
    datos_51.save()
    datos_52.save()
    datos_53.save()
    datos_54.save()
    datos_55.save()
    datos_56.save()
    datos_57.save()
    datos_58.save()
    datos_59.save()
    datos_60.save()
    datos_61.save()
    datos_62.save()
    datos_63.save()
    datos_64.save()
    datos_65.save()
    datos_66.save()
    datos_67.save()
    datos_68.save()
    datos_69.save()
    datos_70.save()
    datos_71.save()
    datos_72.save()
    datos_73.save()
    datos_74.save()
    datos_75.save()
    datos_76.save()
    datos_77.save()
    datos_78.save()
    datos_79.save()
    datos_80.save()
    datos_81.save()
    datos_82.save()
    datos_83.save()
    datos_84.save()
    datos_85.save()
    datos_86.save()
    datos_87.save()
    datos_88.save()
    datos_89.save()
    datos_90.save()
    datos_91.save()
    datos_92.save()
    datos_93.save()
    datos_94.save()
    datos_95.save()
 
    return HttpResponse('CREATE')

def delete(request): 
    #dato = isdbt.objects.get(id=52)
    #dato.delete()
    #isdbt.objects.filter(nombre='ItelTV').delete()
    dato=isdbt.objects.all()
    dato.delete()
    dato1=megafax.objects.all()
    dato1.delete()
    dato2=log.objects.all()
    dato2.delete()
    return HttpResponse('Borrado') 



def actualiz(request):

    dato = isdbt.objects.get(id=10)
    dato.nombre='pepe'

    dato.save()
    return HttpResponse('Actualizado')
"""