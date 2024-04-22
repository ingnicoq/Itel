import pandas as pd
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

conexion_MEGA = mysql.connector.connect(
    host="localhost",
    user="root",
    database=NOMBRE_DB_MEGA,
    port=PORT_MEGA
)
cursor_MEGA = conexion_MEGA.cursor()

conexion_ISDBT = mysql.connector.connect(
    host="localhost",
    user="root",
    database=NOMBRE_DB_ISDBT,
    port=PORT_ISDBT
)
cursor_ISDBT = conexion_ISDBT.cursor()

cursor_ISDBT.execute(f"SELECT * FROM `graficos_isdbt_br` ORDER BY id ASC LIMIT 1")
datos_ISDBT=cursor_ISDBT.fetchone()
fecha_antigua=datetime(datos_ISDBT[1],datos_ISDBT[2],datos_ISDBT[3],datos_ISDBT[4],datos_ISDBT[5],datos_ISDBT[6])
cursor_ISDBT.execute(f"SELECT * FROM `graficos_isdbt_br` ORDER BY id DESC LIMIT 1")
datos_ISDBT=cursor_ISDBT.fetchone()
fecha_actual=datetime(datos_ISDBT[1],datos_ISDBT[2],datos_ISDBT[3],datos_ISDBT[4],datos_ISDBT[5],datos_ISDBT[6])
fecha_borrado = fecha_actual - timedelta(days=10)
cursor_ISDBT.execute(f"SELECT * FROM `graficos_isdbt_br` ORDER BY id ASC")
todo=cursor_ISDBT.fetchall()
id_min=0
for elemento in todo:
    fecha=datetime(elemento[1],elemento[2],elemento[3],elemento[4],elemento[5],elemento[6])
    if fecha < fecha_borrado:
        id_min=elemento[0]
if id_min!=0 :
    cursor_ISDBT.execute(f"DELETE FROM `graficos_isdbt_br` WHERE id<id_min")


#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

cursor_MEGA.execute(f"SELECT * FROM `graficos_megafax_br` ORDER BY id ASC LIMIT 1")
datos_MEGA=cursor_MEGA.fetchone()
fecha_antigua=datetime(datos_MEGA[1],datos_MEGA[2],datos_MEGA[3],datos_MEGA[4],datos_MEGA[5],datos_MEGA[6])
cursor_MEGA.execute(f"SELECT * FROM `graficos_megafax_br` ORDER BY id DESC LIMIT 1")
datos_MEGA=cursor_MEGA.fetchone()
fecha_actual=datetime(datos_MEGA[1],datos_MEGA[2],datos_MEGA[3],datos_MEGA[4],datos_MEGA[5],datos_MEGA[6])
fecha_borrado = fecha_actual - timedelta(days=10)
cursor_MEGA.execute(f"SELECT * FROM `graficos_isdbt_br` ORDER BY id ASC")
todo=cursor_MEGA.fetchall()
for elemento in todo:
    fecha=datetime(elemento[1],elemento[2],elemento[3],elemento[4],elemento[5],elemento[6])
    if fecha < fecha_borrado:
        id_min=elemento[0]
if id_min!=0 :
    cursor_MEGA.execute(f"DELETE FROM `graficos_isdbt_br` WHERE id<id_min")


#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

cursor_ISDBT.execute(f"SELECT * FROM `index_log` ORDER BY id ASC LIMIT 1")
datos_ISDBT=cursor_ISDBT.fetchone()
fecha_antigua=datetime(datos_ISDBT[1],datos_ISDBT[2],datos_ISDBT[3],datos_ISDBT[4],datos_ISDBT[5],datos_ISDBT[6])
cursor_ISDBT.execute(f"SELECT * FROM `index_log` ORDER BY id DESC LIMIT 1")
datos_ISDBT=cursor_ISDBT.fetchone()
fecha_actual=datetime(datos_ISDBT[1],datos_ISDBT[2],datos_ISDBT[3],datos_ISDBT[4],datos_ISDBT[5],datos_ISDBT[6])
fecha_borrado = fecha_actual - timedelta(days=10)
cursor_ISDBT.execute(f"SELECT * FROM `index_log` ORDER BY id ASC")
todo=cursor_ISDBT.fetchall()
id_min=0
for elemento in todo:
    fecha=datetime(elemento[1],elemento[2],elemento[3],elemento[4],elemento[5],elemento[6])
    if fecha < fecha_borrado:
        id_min=elemento[0]

if id_min!=0 :
    cursor_MEGA.execute(f"DELETE FROM `index_log` WHERE id<id_min")

