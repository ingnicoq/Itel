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
PORT=ast.PORT_ISDBT
CANTIDAD_MAX = ast.CANTIDAD_MAX_ISDBT
URL = ast.URL_ISDBT
login_key = ast.login_key_ISDBT
login_value = ast.login_value_ISDBT
LOGIN = {login_key:login_value}
CSV = ast.CSV_MEGA
UBICACION = ast.UBICACION_ISDBT
NOMBRE_PROCESO = ast.NOMBRE_PROCESO_ISDBT
ENCABEZ_MSJ = ast.ENCABEZ_MSJ_ISDBT


def verificar_base_de_datos(host, usuario, nombre_base_datos,puerto):
    try:
        conexion = mysql.connector.connect(
            host=host,
            user=usuario,
            port = puerto
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
    comando = f'''CREATE TABLE IF NOT EXISTS index_isdbt (id INT AUTO_INCREMENT PRIMARY KEY,nombre VARCHAR(50), ip VARCHAR(20), BR_min FLOAT, canal_id VARCHAR(10), estado INT)'''
    cursor.execute(comando)


def generar_log():
    comando = f'''CREATE TABLE IF NOT EXISTS index_log (id INT AUTO_INCREMENT PRIMARY KEY,year INT, month INT, day INT, hour INT, min INT, sec INT,log TEXT)'''
    cursor.execute(comando)


def insertar_datos_canal_datos(id, nombre,ip,br_min,canal_id): 
    cursor.execute("INSERT INTO index_isdbt (id,nombre,ip,BR_min,canal_id,estado) VALUES (%s,%s,%s,%s,%s,0)", (id,nombre, ip, br_min,canal_id))

def buscar_en_CSV(canal):
    df = leer_csv()
    for index, row in df.iterrows():
        if canal == row['nombre']:
            return row['ip'],float(row['BR_min'])
    return '0.0.0.0',0.5  
  
def existe_tabla_index():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        database=NOMBRE_DB,
        port=PORT
    )

    cursor = conexion.cursor()

    cursor.execute("SHOW TABLES")
    tablas = cursor.fetchall()
    nombre = 'index_isdbt'
    for tabname in tablas:
        if nombre in tabname:
            return True

    return False


def existe_tabla_log():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        database=NOMBRE_DB,
        port=PORT
    )

    cursor = conexion.cursor()

    cursor.execute("SHOW TABLES")
    tablas = cursor.fetchall()
    nombre = 'index_log'
    for tabname in tablas:
        if nombre in tabname:
            return True

    return False

def buscar_canal_tabla(canal):
    try:
        cursor.execute(f"SELECT id FROM `index_isdbt` WHERE nombre=%s",[str(canal)])
        valor=cursor.fetchone()[0]
        if valor!="":
            return True
    except:
        return False

def buscar_registro_tabla(posicion):
    try:
        cursor.execute(f"SELECT nombre FROM `index_isdbt` WHERE id=%s",[str(posicion)])
        valor=cursor.fetchone()[0]
        if valor!="":
            return True
    except:
        return False


try:
    if not verificar_base_de_datos("localhost", "root", NOMBRE_DB,PORT):

        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
        )

        cursor = conexion.cursor()
        creacion_db(NOMBRE_DB)
        cursor.close()
        conexion.close()
        
    conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            database=NOMBRE_DB,
            port = 3307
        )
    cursor = conexion.cursor()
    canales = leer_datos_mux()
    longitud = len(canales)
    if not existe_tabla_index():
        generar_canal_datos()
    if not existe_tabla_log():
        generar_log()
   
    i=1
    for canal in canales: 
        if canal != None:  
            if  buscar_registro_tabla(i):
                if not buscar_canal_tabla(canal):
                    
                        ip,br = buscar_en_CSV(canal)
                        insertar_datos_canal_datos(i,canal,ip,br,str(f"canal_{i}"))
                        conexion.commit()
            else:
                
                        ip,br = buscar_en_CSV(canal)
                        insertar_datos_canal_datos(i,canal,ip,br,str(f"canal_{i}"))
                        conexion.commit()
        i+=1
        
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        database=NOMBRE_DB
        )
    cursor.close()
    conexion.close()
        
except Exception as e:
    print(f"Error en la inicializacion de la DB. ERROR: {e}")
