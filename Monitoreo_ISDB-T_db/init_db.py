import mysql.connector
import pandas as pd
from datetime import datetime
import requests
from itertools import zip_longest
import re
import sys
import os
ruta_padre = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ruta_padre)
import autostart_monitoreo as ast

NOMBRE_DB = ast.NOMBRE_DB_ISDBT
CANTIDAD_MAX = ast.CANTIDAD_MAX_ISDBT
URL = ast.URL_ISDBT
login_key = ast.login_key_ISDBT
login_value = ast.login_value_ISDBT
LOGIN = {login_key:login_value}
CSV = ast.CSV_MEGA
UBICACION = ast.UBICACION_ISDBT
NOMBRE_PROCESO = ast.NOMBRE_PROCESO_ISDBT
ENCABEZ_MSJ = ast.ENCABEZ_MSJ_ISDBT


def verificar_base_de_datos(host, usuario, nombre_base_datos):
    try:
        conexion = mysql.connector.connect(
            host=host,
            user=usuario,
        )
        cursor = conexion.cursor()

        cursor.execute("SHOW DATABASES")
        bases_de_datos = cursor.fetchall()

        for base_de_datos in bases_de_datos:
            if nombre_base_datos in base_de_datos:
                return True

        cursor.close()
        conexion.close()
    except mysql.connector.Error as error:
        print("Error al conectar al servidor MySQL:", error)
    return False

def replace_ascii(text):
    if text is None:
        return text  
    def inner_replace(match):
        
        hex_number = match.group(1)
        
        return chr(int(hex_number, 16))

    return re.sub(r'%([0-9a-fA-F]+)', inner_replace, text)\

def leer_datos_mux():
    contador=0
    contenido=''
    
    for i in range (0,16):
        variable='hInIPSel='+str(i)
        respuesta=requests.post(URL,headers=LOGIN,data=variable)

        if respuesta.status_code == 200:

            ubicacion = respuesta.text.find('Out')
            respuesta = respuesta.text[0:ubicacion:1]
            contenido=contenido+respuesta
        
        else:
            print(f"Error al realizar la solicitud. Código de estado: {respuesta.status_code}")
    
    contenido = contenido.replace(':','\n')
    contenido = contenido.replace(';',',')
    ubicacion = contenido.find('Out')
    contenido = contenido[0:ubicacion:1]
    todo = 'IN,Entrada,IP,1,2,Habilitado,Bit Rate,8,9,10,Nombre Canal,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35\n'+contenido
    lineas = todo.split('\n')
    datos = [linea.split(',') for linea in lineas]

    max_columns = max(len(linea) for linea in datos)
    data_filled = list(zip_longest(*datos, fillvalue=None))


    df = pd.DataFrame(datos[1:], columns=datos[0])

    df['Nombre Canal'] = df['Nombre Canal'].apply(replace_ascii)
    canales=[]
    for index, row in df.iterrows():
        if contador<= CANTIDAD_MAX:
            canales.append(row['Nombre Canal'])
            contador+=1
    return canales

def leer_csv():
    df=pd.read_csv(CSV)
    return df

def creacion_db(nombre_db):
    comando = f"CREATE DATABASE IF NOT EXISTS {nombre_db}"
    cursor.execute(comando)
    conexion.close()


def generar_canal_datos():
    comando = f'''CREATE TABLE IF NOT EXISTS canal_datos (id INT AUTO_INCREMENT PRIMARY KEY,nombre VARCHAR(50), ip VARCHAR(20), BR_min FLOAT, canal_id VARCHAR(10), estado INT)'''
    cursor.execute(comando)


def generar_log():
    comando = f'''CREATE TABLE IF NOT EXISTS log (id INT AUTO_INCREMENT PRIMARY KEY,year INT, month INT, day INT, hour INT, min INT, sec INT,log TEXT)'''
    cursor.execute(comando)


def generar_tablas(cantidad):
    for i in range(1,cantidad+1):
        comando = f'''CREATE TABLE IF NOT EXISTS canal_{i} (id INT AUTO_INCREMENT PRIMARY KEY,year INT, month INT, day INT, hour INT, min INT, sec INT, BR FLOAT)'''
        cursor.execute(comando)


def insertar_datos_canal_datos(nombre,ip,br_min,canal_id): 
    cursor.execute("INSERT INTO canal_datos (nombre,ip,BR_min,canal_id,estado) VALUES (%s,%s,%s,%s,0)", (nombre, ip, br_min,canal_id))

def buscar_en_CSV(canal):
    df = leer_csv()
    for index, row in df.iterrows():
        if canal == row['nombre']:
            return row['ip'],float(row['BR_min'])
    return '0.0.0.0',0.5  
  
try:
    if not verificar_base_de_datos("localhost", "root", NOMBRE_DB):

        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
        )

        cursor = conexion.cursor()
        creacion_db(NOMBRE_DB)
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            database=NOMBRE_DB
        )
        cursor = conexion.cursor()
        canales = leer_datos_mux()
        longitud = len(canales)
        generar_tablas(longitud)
        generar_canal_datos()
        generar_log()
        i=1
        for canal in canales:
            ip,br = buscar_en_CSV(canal)
            insertar_datos_canal_datos(canal,ip,br,str(f"canal_{i}"))
            i+=1
            conexion.commit()
    conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            database=NOMBRE_DB
        )
            
except Exception as e:
    print(f"Error en la inicializacion de la DB. ERROR: {e}")
