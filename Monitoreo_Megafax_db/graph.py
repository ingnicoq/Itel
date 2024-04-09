import pandas as pd
import numpy as nu
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import mysql.connector
import sys
import os
ruta_padre = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ruta_padre)
import autostart_monitoreo as ast

NOMBRE_DB = ast.NOMBRE_DB_MEGA
CANTIDAD_MAX = ast.CANTIDAD_MAX_MEGA
URL = ast.URL_MEGA
login_key = ast.login_key_MEGA
login_value = ast.login_value_MEGA
LOGIN = {login_key:login_value}
CSV = ast.CSV_MEGA
UBICACION = ast.UBICACION_MEGA
NOMBRE_PROCESO = ast.NOMBRE_PROCESO_MEGA
ENCABEZ_MSJ = ast.ENCABEZ_MSJ_MEGA

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    database=NOMBRE_DB
)
cursor = conexion.cursor()


def calculo_fecha(opcion,ultima_fecha):
     if opcion==1:
        fecha_anterior = ultima_fecha - timedelta(days=7)
        titulo = '7 dias'
     elif opcion==2:
        fecha_anterior = ultima_fecha - timedelta(days=1)
        titulo = '1 dia'
     elif opcion==3:
        fecha_anterior = ultima_fecha - timedelta(hours=6)
        titulo = '6 horas'
     elif opcion==4:
        fecha_anterior = ultima_fecha - timedelta(hours=1)
        titulo = '1 hora'
  
     return fecha_anterior,titulo


def consulta_nombre_tabla(nombre_canal):
    try:
        cursor.execute(f'''SELECT * FROM `canal_datos` WHERE `nombre`='{nombre_canal}';''')
        respuesta = cursor.fetchall()              
        return respuesta[0][4],respuesta[0][3]
    except Exception as e:
        print("ERROR consulta nombre tabla")

def importar_datos_bd(nombre_tabla):
    try:
        cursor.execute(f'''SELECT * FROM `{nombre_tabla}`''')
        respuesta = cursor.fetchall()              
        return respuesta
    except Exception as e:
        print("ERROR importar datos bd")

    
def mostrar_grafico(ax,seleccion_combobox,opcion):

   nombre_tabla,BR_min = consulta_nombre_tabla(seleccion_combobox)
   datos = importar_datos_bd(nombre_tabla)
   

   tiempo = []
   BR = []
   cons = BR_min
   auxiliar=datos[-1]
   ultima_fecha=datetime(int(auxiliar[1]), int(auxiliar[2]), int(auxiliar[3]),int(auxiliar[4]), int(auxiliar[5]), int(auxiliar[6]))
   
   fecha_anterior,titulo=calculo_fecha(opcion,ultima_fecha)
   

   for elemento in datos:
      auxiliar = datetime(int(elemento[1]), int(elemento[2]), int(elemento[3]),int(elemento[4]), int(elemento[5]), int(elemento[6]))
      
    
      if auxiliar >= fecha_anterior:
         tiempo.append(auxiliar)
         BR.append(float(elemento[7]))

   ax.set_title(titulo, fontsize=10, loc='right')
   ax.plot(tiempo, BR)
   ax.tick_params(axis='x', labelsize=8, rotation=45)
   ax.tick_params(axis='y', labelsize=8)
   ax.set_ylabel('BR')
   

   ax.axhline(y=cons, color='r', linestyle='--', label='BR_MIN')
   ax.legend()
   del ax
   del datos
   del tiempo
   del BR


