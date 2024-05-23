import requests
import pandas as pd
from itertools import zip_longest
import re
from os import system
import time
from datetime import datetime
import mysql.connector
import init_db
import sys
import os
ruta_padre = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ruta_padre)
import autostart_monitoreo as ast

NOMBRE_DB = ast.NOMBRE_DB_MEGA
PORT = ast.PORT_MEGA
CANTIDAD_MAX = ast.CANTIDAD_MAX_MEGA
URL = ast.URL_MEGA
login_key = ast.login_key_MEGA
login_value = ast.login_value_MEGA
CHAT_ID=ast.CHAT_ID_MEGA
LOGIN = {login_key:login_value}
CSV = ast.CSV_MEGA
UBICACION = ast.UBICACION_MEGA
NOMBRE_PROCESO = ast.NOMBRE_PROCESO_MEGA
ENCABEZ_MSJ = ast.ENCABEZ_MSJ_MEGA


init_db


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)



conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    database=NOMBRE_DB,
    port=PORT
)
cursor = conexion.cursor()


class Colores:
    NEGRITA = '\033[1m'
    RESET = '\033[0m'
    SUBRAYADO = '\033[4m'
    ROJO = '\033[91m'
    VERDE = '\033[92m'


def escribir_log(texto):
    try:
        now = datetime.now()
        texto=texto + "--> MEGAFAX"
        cursor.execute(f"INSERT INTO index_log (year, month, day, hour, min, sec, log) VALUES (%s, %s, %s, %s, %s, %s, %s)", (now.year, now.month, now.day, now.hour, now.minute, now.second, texto))
        conexion.commit()
        return 0
    except:
        print(str(now)+"--->Error en escribir LOG")
        return 


def leer_estado(id):
    try:
        cursor.execute(f"SELECT estado FROM `index_megafax` WHERE id=%s",[str(id)])
        valor=cursor.fetchone()[0]
        
        return valor
    except Exception as e:
        texto='Error leer_estado: '+str(e)
        escribir_log(texto)
        return 


def escribir_estado(id,estado):
    try:
        cursor.execute(f"UPDATE index_megafax SET estado=%s WHERE id=%s",[str(estado),str(id)])
        return
    except Exception as e:
        texto='Error escribir_estado: '+str(e)
        escribir_log(texto)
        return 



def enviar_mensaje(lista,aux):
    try:
        if aux ==1:
            mensaje=ENCABEZ_MSJ+'\n\nCanales Cortados:\n\t'
        elif aux == 2:
            mensaje=ENCABEZ_MSJ+'\n\nCanales Operativos:\n\t'
        
        resultado = '\n\t'.join(lista)
        mensaje=mensaje+resultado

           
        requests.post('https://api.telegram.org/bot6682970550:AAE4cg-GbbKUgIMcM4mYcNl87Q3xa2HIqeE/sendMessage', data={'chat_id': {str(CHAT_ID)}, 'text': {mensaje}})   
        time.sleep(0.1)
       
        del mensaje
        del resultado
        
    except Exception as e:
        texto='Error envio Telegram: '+str(e)
        escribir_log(texto)
        return 


def replace_ascii(text):
    try:
        if text is None:
            return text  
        def inner_replace(match):
            
            hex_number = match.group(1)
            
            return chr(int(hex_number, 16))
        return re.sub(r'%([0-9a-fA-F]+)', inner_replace, text)\
        
    except Exception as e:
        texto='Error reemplazo caracter: '+str(e)
        escribir_log(texto)
        return 
    

def encontrar_BR(num):
    try:
        if num == "":
            return 2
        registro = BR_Min_dict[num]
        if registro:
            valor=registro
        else:
            valor=2.5
        valor = float(valor)
        return valor
    
    except Exception as e:
        texto='Error encontrar BR: '+str(e)
        escribir_log(texto)
        return 
    
    
def escribir_db(entrada, bitrate):
    
    try:
        now = datetime.now()
        bitrate=round(bitrate,2)
        cursor.execute("SELECT canal_id FROM index_megafax WHERE id = %s;", [str(entrada)])
        tabla = cursor.fetchone()[0]
        cursor.execute(f"INSERT INTO graficos_megafax_br (year, month, day, hour, min, sec, BR,canal_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (now.year, now.month, now.day, now.hour, now.minute, now.second, bitrate,tabla))
        conexion.commit()
    except Exception as e:
        texto='Error escribir DB: '+str(e)
        escribir_log(texto)
        return 

def consulta_ip():
    try:
        cursor.execute("SELECT nombre, ip FROM index_megafax")
        tabla = cursor.fetchall()
        datos_ip = []
        for fila in tabla:
            datos_ip.append(fila)
        return datos_ip
    except Exception as e:
        texto='Error consulta IP: '+str(e)
        escribir_log(texto)
        return 


def consulta_BR_min():
    try:
        cursor.execute("SELECT id, BR_min FROM index_megafax")
        tabla = cursor.fetchall()
        datos_br_min = []
        for fila in tabla:
            datos_br_min.append(fila)
        return datos_br_min
    except Exception as e:
        texto='Error consulta BR Min: '+str(e)
        escribir_log(texto)
        return 
    
def encontrar_nombre(numero):
    try:
        cursor.execute("SELECT nombre FROM index_megafax WHERE id = %s;", [str(numero)])
        nombre = cursor.fetchone()[0]
        return nombre
    except:
        return ""
    
def verificacion_tabla(posicion,nombre_mux):
    try:
        cursor.execute("SELECT MAX(id) FROM index_megafax")
        max_channel=cursor.fetchall()[0]
        if posicion < max_channel[0]+1:
            nombre=encontrar_nombre(posicion)
            if nombre_mux != nombre:
                cursor.execute("UPDATE index_megafax SET nombre = %s WHERE nombre = %s",(nombre_mux,nombre))
                conexion.commit()
        else:
            cursor.execute(f"INSERT INTO index_megafax (id,nombre,ip,BR_min,canal_id) VALUES (%s,%s, %s, %s, %s)",(str(max_channel[0]+1),nombre_mux, "0.0.0.0", str(0.5), f"canal_{posicion}"))
            conexion.commit()
    except Exception as e:
        texto='Error verificacion tabla: '+str(e)
        escribir_log(texto)
        return 



BR_Min = consulta_BR_min()
canales_dic={}

for elemento in BR_Min:
    canales_dic[elemento[0]]={'Cont_Alarm':0,'Estado_ant':0,'Estado_act':0,'BR_acum':0,'Cont_WR':0}
    estado = leer_estado(elemento[0])
    canales_dic[elemento[0]]['Estado_ant']=estado
  

while True:

    now=datetime.now()
    print(now,"---- MEGAFAX")

    BR_Min = consulta_BR_min()
    for elemento in BR_Min:
        estado = leer_estado(elemento[0])
        canales_dic[elemento[0]]['Estado_ant']=estado


    
    #print('Debug MSJ: Inicio While true')
    contenido=''
    ips = consulta_ip()
    ips_dict = dict(ips)
    BR_Min=consulta_BR_min()
    BR_Min_dict=dict(BR_Min)

    #print('Debug MSJ: Inicio For')
    for i in range (0,16):
        try:
            variable='hInIPSel='+str(i)
            respuesta=requests.post(URL,headers=LOGIN,data=variable)
            #print(f'Debug MSJ: Reuqest Nº {i}')

            if respuesta.status_code == 200:

                ubicacion = respuesta.text.find('Out')
                respuesta = respuesta.text[0:ubicacion:1]
                contenido=contenido+respuesta
                #print(f'Debug MSJ: Respuesta correcta Nº {i}')
            
            else:
                print(f"Error al realizar la solicitud. Código de estado: {respuesta.status_code}")
        except Exception as e:
            escribir_log(e)
            continue
        time.sleep(0.05)

    #print('Debug MSJ: Fin bucle For')
    try:
        canales_conrtados=[]
        canales_operativos=[]

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

        
        df['IP'] = df['Nombre Canal'].map(ips_dict.get)
        #print('Debug MSJ: Fin Acondicionamiento de datos')
    except Exception as e:
        texto='Error formateo de datos: '+str(e)
        escribir_log(texto)
        continue 

    #system("clear")
    #print(f"|{Colores.SUBRAYADO}{Colores.NEGRITA}{'Nombre del Canal':<30}|{'BR MIN':<10}|{'Bit Rate':<10}|{'IP':>17}{Colores.RESET}|")    
    #print('Debug MSJ: Inicio FOR sobre DF')
    
    for index, row in df.iterrows():
        try:

            if row['Habilitado']=='1':
                posicion=(int(row['Entrada'])+1)
                verificacion_tabla(posicion,row['Nombre Canal'])
                auxiliar = encontrar_BR(posicion)
                BR_num=row['Bit Rate']
                BR_num=float(BR_num[0:(len(BR_num)-1)])
                canales_dic[posicion]['Cont_WR']+=1
                if canales_dic[posicion]['Cont_WR']<4:
                    canales_dic[posicion]['BR_acum']+= BR_num
                    
                else:
                    
                    canales_dic[posicion]['BR_acum']+= BR_num
                    escribir_db(posicion,(canales_dic[posicion]['BR_acum']/4))
                    canales_dic[posicion]['BR_acum']=0
                    canales_dic[posicion]['Cont_WR']=0

                if (BR_num < auxiliar):
                    #print(f"|{Colores.SUBRAYADO}{row['Nombre Canal']:<30}|{Colores.SUBRAYADO}{auxiliar:<10}|{Colores.SUBRAYADO}{Colores.ROJO}{row['Bit Rate']:<10}{Colores.RESET}|{Colores.SUBRAYADO}{row['IP']:>17}{Colores.RESET}|")
                    canales_dic[posicion]['Cont_Alarm'] +=1
                else:
                    #print(f"|{Colores.SUBRAYADO}{row['Nombre Canal']:<30}|{Colores.SUBRAYADO}{auxiliar:<10}|{Colores.SUBRAYADO}{Colores.VERDE}{row['Bit Rate']:<10}{Colores.RESET}|{Colores.SUBRAYADO}{row['IP']:>17}{Colores.RESET}|")
                    canales_dic[posicion]['Cont_Alarm'] =0
                    canales_dic[posicion]['Estado_act'] =0
                    #canales_dic[posicion]['Estado_ant']=leer_estado(posicion)
                    if canales_dic[posicion]['Estado_act']!=canales_dic[posicion]['Estado_ant']:
                        canales_operativos.append(row['Nombre Canal'])
                    canales_dic[posicion]['Estado_ant']=0
                    escribir_estado(posicion,0)

        except Exception as e:
            print(e,row['Nombre Canal'])
            texto='Error procesamiento de datos: '+str(e)
            escribir_log(texto)
            continue

    #print('Debug MSJ: FIN FOR sobre DF')
    

    try:
        contador_posicion_dic=1
        for clave,valor in canales_dic.items():
            if valor['Cont_Alarm']>=6:
                valor['Estado_act']=1
                #valor['Estado_ant']=leer_estado(contador_posicion_dic)
                if valor['Estado_act']!=valor['Estado_ant']:
                    nombre = encontrar_nombre(clave)
                    canales_conrtados.append(nombre)
                valor['Estado_ant']=1
                escribir_estado(contador_posicion_dic,1)
            contador_posicion_dic+=1
        

        if len(canales_conrtados)!=0:
            enviar_mensaje(canales_conrtados,1)
        
        if len(canales_operativos)!=0:
            enviar_mensaje(canales_operativos,2)

    except Exception as e:
        texto='Error analisis de datos para msj: '+str(e)
        escribir_log(texto)


    #print('Debug MSJ: Inicio Borrado variables')
    try:
        del auxiliar
        del contenido
        del df
        del ips
        del BR_Min
        del canales_conrtados
        del canales_operativos
    except:
        texto="Error el borrar variables"
        print(texto)
        escribir_log(texto)
        continue

    #print('Debug MSJ: Fin Bucle While')
    time.sleep(10)
    








