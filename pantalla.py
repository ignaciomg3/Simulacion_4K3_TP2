import tkinter as tk
from tkinter import ttk
from funciones import *
from src.Generadores.generadorCongruencialLineal import GeneradorCongruencial

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from src.Generadores import *
import seaborn as sns
from tkinter import messagebox

class PantallaPrincipal:
    def __init__(self, root):
        """Inicializa la pantalla principal de la aplicación."""
        self.root = root    
        self.root.title("Simulador de Distribuciones Aleatorias")
        self.root.geometry("1200x800")
        
        # Variables para almacenar la configuración
        self.distribucion_seleccionada = tk.StringVar(value="Uniforme")
        self.cantidad_numeros = tk.StringVar(value="1000")
        self.num_intervalos = tk.StringVar(value="10")
        self.param1 = tk.StringVar(value="0")
        self.param2 = tk.StringVar(value="1")
        # Inicializar los parámetros lbl_param1, lbl_param2, entry_param2
        self.lbl_param1 = ttk.Label(self.root, text="Parámetro 1:")
        self.lbl_param1.pack()
        
        self.lbl_param2 = ttk.Label(self.root, text="Parámetro 2:")
        self.lbl_param2.pack()
        
        self.entry_param2 = ttk.Entry(self.root, textvariable=self.param2)
        self.entry_param2.pack()
        
        
        
        # Variables para almacenar resultados
        self.numeros_generados = []
        
        # Crear el generador congruencial lineal
        self.generador = GeneradorCongruencial(
            semilla=12345,
            a=1103515245,
            c=12345,
            m=2**31
        )
        
        # Crear frames llamando funciones externas
        crear_frame_configuracion(self, self.distribucion_seleccionada, self.cantidad_numeros, self.num_intervalos, self.param1, self.param2)
        crear_frame_grafico(self)
        crear_frame_tabla(self)
        
        # Actualizar etiquetas de parámetros según distribución inicial
        actualizar_etiquetas_parametros(self, self.distribucion_seleccionada, self.lbl_param1, self.lbl_param2, self.entry_param2, self.param1, self.param2)
    
        """Actualiza las etiquetas de los parámetros según la distribución seleccionada"""
        distribucion = self.distribucion_seleccionada.get()
        
        if distribucion == "Uniforme":
            self.lbl_param1.configure(text="Límite inferior (a):")
            self.lbl_param2.configure(text="Límite superior (b):")
            self.entry_param2.configure(state="normal")
            self.param1.set("0")
            self.param2.set("1")
        
        elif distribucion == "Exponencial":
            self.lbl_param1.configure(text="Lambda (λ):")
            self.lbl_param2.configure(text="")
            self.entry_param2.configure(state="disabled")
            self.param1.set("1")
            self.param2.set("")
        
        elif distribucion == "Normal":
            self.lbl_param1.configure(text="Media (μ):")
            self.lbl_param2.configure(text="Desviación estándar (σ):")
            self.entry_param2.configure(state="normal")
            self.param1.set("0")
            self.param2.set("1")
    

    

    
