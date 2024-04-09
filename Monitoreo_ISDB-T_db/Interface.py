import tkinter as tk
import pandas as pd
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import graph
import mysql.connector
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



conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    database=NOMBRE_DB
)
cursor = conexion.cursor()


def lista_canales():
    try:
        lista_canales=[]
        cursor.execute(f'''SELECT * FROM `canal_datos`''')
        respuesta = cursor.fetchall()  
        for elemento in respuesta:
            lista_canales.append(elemento[1])            
        return lista_canales
    except Exception as e:
        print("ERROR obtencion lista canales")

list_canales = lista_canales()


class AplicacionGUI:


    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación con GUI y Gráfico")

        opciones = list_canales
        self.seleccion_combobox = tk.StringVar()  # Variable para almacenar la selección
        self.combo = ttk.Combobox(self.root, values=opciones, textvariable=self.seleccion_combobox)
        self.combo.pack(pady=10)
        
        btn_mostrar_grafico = ttk.Button(root, text="Mostrar Gráfico", command=self.mostrar_grafico)
        btn_mostrar_grafico.pack(pady=10)

        self.figura = Figure(figsize=(12, 6), dpi=100)
        self.graficos = [] 
        self.variables = [1,2,3,4]

        for i in range(4): 
            grafico = self.figura.add_subplot(2, 2, i + 1)
            self.graficos.append(grafico)

        self.canvas = FigureCanvasTkAgg(self.figura, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack()

        self.figura.subplots_adjust(hspace=0.5)

    

    def mostrar_grafico(self):
        seleccion_combobox = self.seleccion_combobox.get()
        for i, grafico in enumerate(self.graficos):
            grafico.clear()
            grafico.set_ylim(0, 20)
            graph.mostrar_grafico(grafico, seleccion_combobox,self.variables[i]) 
        self.canvas.draw()

        

    def mostrar_seleccion(self):
        seleccion = self.combo.get()


if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionGUI(root)
    root.mainloop()