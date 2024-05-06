import subprocess
import time
import pandas as pd
import psutil
import signal
import os
from datetime import datetime, timedelta
import mysql.connector

df=pd.read_json("constants.json")


NOMBRE_DB_MEGA = df["Megafax"]["nombre_db"]
PORT_MEGA = df["Megafax"]["port"]
CANTIDAD_MAX_MEGA = df["Megafax"]["cant_max"]
URL_MEGA = df["Megafax"]["url"]
login_key_MEGA = df["Megafax"]["login_key"]
login_value_MEGA = df["Megafax"]["login_value"]
CHAT_ID_MEGA=df["Megafax"]["chat_id"]
LOGIN_MEGA = {login_key_MEGA: login_value_MEGA}
CSV_MEGA = df["Megafax"]["csv"]
UBICACION_MEGA = df["Megafax"]["ubicacion"]
NOMBRE_PROCESO_MEGA = df["Megafax"]["nombre_proceso"]
ENCABEZ_MSJ_MEGA = df["Megafax"]["encab_msj"]


NOMBRE_DB_ISDBT = df["ISDB-T"]["nombre_db"]
PORT_ISDBT = df["ISDB-T"]["port"]
CANTIDAD_MAX_ISDBT = df["ISDB-T"]["cant_max"]
URL_ISDBT = df["ISDB-T"]["url"]
login_key_ISDBT = df["ISDB-T"]["login_key"]
login_value_ISDBT = df["ISDB-T"]["login_value"]
CHAT_ID_ISDBT=df["ISDB-T"]["chat_id"]
LOGIN_ISDBT = {login_key_MEGA: login_value_MEGA}
CSV_ISDBT = df["ISDB-T"]["csv"]
UBICACION_ISDBT = df["ISDB-T"]["ubicacion"]
NOMBRE_PROCESO_ISDBT = df["ISDB-T"]["nombre_proceso"]
ENCABEZ_MSJ_ISDBT = df["ISDB-T"]["encab_msj"]



def check_process(pid):
    for proc in psutil.process_iter(['pid']):
        if proc.info['pid'] == pid:
            return True
    return False
    
def start_process(process_path):
    process=subprocess.Popen(["python3", process_path])
    pid=process.pid
    time.sleep(5)
    return pid

def terminar_process(pid):
    try:
        os.kill(pid, signal.SIGTERM)
        print("Proceso con PID {} terminado exitosamente.".format(pid))
        time.sleep(5)
    except ProcessLookupError:
        print("El proceso con PID {} no fue encontrado.".format(pid))
    

def limpiar_registros_isdbt():

    conexion_ISDBT = mysql.connector.connect(
        host="localhost",
        user="root",
        database=NOMBRE_DB_ISDBT,
        port=PORT_ISDBT
    )
    cursor_ISDBT = conexion_ISDBT.cursor()
    try:
        bandera=1
        while(bandera==1):
            cursor_ISDBT.execute(f"SELECT * FROM `graficos_isdbt_br` ORDER BY id ASC LIMIT 1 OFFSET 1")
            datos_ISDBT=cursor_ISDBT.fetchone()
            fecha_antigua=datetime(datos_ISDBT[1],datos_ISDBT[2],datos_ISDBT[3],datos_ISDBT[8],datos_ISDBT[4],datos_ISDBT[5])
            cursor_ISDBT.execute(f"SELECT * FROM `graficos_isdbt_br` ORDER BY id DESC LIMIT 1")
            datos_ISDBT=cursor_ISDBT.fetchone()
            ultimo_id= datos_ISDBT[0]
            fecha_actual=datetime(datos_ISDBT[1],datos_ISDBT[2],datos_ISDBT[3],datos_ISDBT[8],datos_ISDBT[4],datos_ISDBT[5])
            fecha_borrado = fecha_actual - timedelta(days=8)

            if fecha_antigua<fecha_borrado:
                cursor_ISDBT.execute(f"SELECT * FROM `graficos_isdbt_br` ORDER BY id ASC LIMIT 1500")
                todo=cursor_ISDBT.fetchall()

                for elemento in todo:
                    fecha=datetime(elemento[1],elemento[2],elemento[3],elemento[8],elemento[4],elemento[5])
                    if fecha < fecha_borrado:
                        id_min=elemento[0]
                    
                cursor_ISDBT.execute("DELETE FROM `graficos_isdbt_br` WHERE id < %s" % id_min)
                conexion_ISDBT.commit()
            else:
                bandera=0
        
        cursor_ISDBT.execute(f"SELECT * FROM `graficos_isdbt_br` ORDER BY id ASC LIMIT 1 OFFSET 1")
        datos_ISDBT=cursor_ISDBT.fetchone()
        if datos_ISDBT[0] != 1:
            cursor_ISDBT.execute(f"SELECT * FROM `graficos_isdbt_br` ORDER BY id ASC")
            todo=cursor_ISDBT.fetchall()
            contador=1
            for elemento in todo:
                if elemento[0] <= ultimo_id:
                    cursor_ISDBT.execute("UPDATE `graficos_isdbt_br` SET id = %s WHERE id = %s",(str(contador),str(elemento[0])))
                    contador+=1
                else:
                    break

        conexion_ISDBT.commit()
    except Exception as e:
        print("Error al borrar isdb-t")
        print(e)

    return


def limpiar_registros_mega():

    conexion_MEGA = mysql.connector.connect(
    host="localhost",
    user="root",
    database=NOMBRE_DB_MEGA,
    port=PORT_MEGA
    )
    cursor_MEGA = conexion_MEGA.cursor()

    try:
        bandera=1
        while(bandera==1):
            cursor_MEGA.execute(f"SELECT * FROM `graficos_megafax_br` ORDER BY id ASC LIMIT 1 OFFSET 1")
            datos_MEGA=cursor_MEGA.fetchone()
            fecha_antigua=datetime(datos_MEGA[1],datos_MEGA[2],datos_MEGA[3],datos_MEGA[8],datos_MEGA[4],datos_MEGA[5])
            cursor_MEGA.execute(f"SELECT * FROM `graficos_megafax_br` ORDER BY id DESC LIMIT 1")
            datos_MEGA=cursor_MEGA.fetchone()
            ultimo_id= datos_MEGA[0]
            fecha_actual=datetime(datos_MEGA[1],datos_MEGA[2],datos_MEGA[3],datos_MEGA[8],datos_MEGA[4],datos_MEGA[5])
            fecha_borrado = fecha_actual - timedelta(days=8)

            if fecha_antigua<fecha_borrado:
                cursor_MEGA.execute(f"SELECT * FROM `graficos_megafax_br` ORDER BY id ASC LIMIT 1500")
                todo=cursor_MEGA.fetchall()

                for elemento in todo:
                    fecha=datetime(elemento[1],elemento[2],elemento[3],elemento[8],elemento[4],elemento[5])
                    if fecha < fecha_borrado:
                        id_min=elemento[0]
                    
                cursor_MEGA.execute("DELETE FROM `graficos_megafax_br` WHERE id < %s" % id_min)
                conexion_MEGA.commit()
            else:
                bandera=0
        
        cursor_MEGA.execute(f"SELECT * FROM `graficos_megafax_br` ORDER BY id ASC LIMIT 1 OFFSET 1")
        datos_MEGA=cursor_MEGA.fetchone()
        if datos_MEGA[0] != 1:
            cursor_MEGA.execute(f"SELECT * FROM `graficos_megafax_br` ORDER BY id ASC")
            todo=cursor_MEGA.fetchall()
            contador=1
            for elemento in todo:
                if elemento[0] <= ultimo_id:
                    cursor_MEGA.execute("UPDATE `graficos_megafax_br` SET id = %s WHERE id = %s",(str(contador),str(elemento[0])))
                    contador+=1
                else:
                    break

        conexion_MEGA.commit()
    except Exception as e:
        print("Error al borrar Megafax")
        print(e)

    return

hora_borrado = "03:00"
contador = 0
if __name__ == "__main__":

    script_path_isdbt = UBICACION_ISDBT
    process_name_isdbt = NOMBRE_PROCESO_ISDBT 
    pid_isdbt = start_process(script_path_isdbt)

    script_path_mega = UBICACION_MEGA
    process_name_mega = NOMBRE_PROCESO_MEGA 
    pid_mega = start_process(script_path_mega)

    while True:

        
        if not check_process(pid_isdbt):
            terminar_process(pid_isdbt)
            print(f"El proceso {process_name_isdbt} no está en ejecución. Reiniciando...")
            pid_isdbt = start_process(script_path_isdbt)
            contador=0

        if not check_process(pid_mega):
            terminar_process(pid_mega)
            print(f"El proceso {process_name_mega} no está en ejecución. Reiniciando...")
            pid_mega = start_process(script_path_mega)
            contador=0

        if not contador < 5:
            terminar_process(pid_mega)
            pid_mega=start_process(script_path_mega)
            
            terminar_process(pid_isdbt)
            pid_isdbt=start_process(script_path_isdbt)
            contador=0

        hora_actual = datetime.now().time()
        hora_minutos = hora_actual.strftime('%H:%M')

        if hora_minutos == hora_borrado:
            terminar_process(pid_mega)
            pid_mega=start_process(script_path_mega)
            terminar_process(pid_isdbt)
            pid_isdbt=start_process(script_path_isdbt)
            contador=0
            limpiar_registros_isdbt()
            limpiar_registros_mega()
            print("Registros Borrados y Reordenados")
            contador_borrado = 0
        
        time.sleep(60)
        contador+=1
        