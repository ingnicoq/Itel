import subprocess
import time
import pandas as pd
import psutil
import signal
import os
import limpiar_registros

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
    except ProcessLookupError:
        print("El proceso con PID {} no fue encontrado.".format(pid))
    
contador_borrado = 0
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
            pid = start_process(script_path_isdbt)
            contador=0

        if not check_process(pid_mega):
            terminar_process(pid_mega)
            print(f"El proceso {process_name_mega} no está en ejecución. Reiniciando...")
            pid = start_process(script_path_mega)
            contador=0

        if not contador < 5:
            terminar_process(pid_mega)
            pid=start_process(script_path_mega)
            
            terminar_process(pid_isdbt)
            pid=start_process(script_path_isdbt)
            contador=0

        if not contador_borrado < 1440:
            limpiar_registros
            contador_borrado = 0
        
        time.sleep(60)
        contador+=1
        contador_borrado+=1