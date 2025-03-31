import tkinter as tk
from pantalla import PantallaPrincipal
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
import sys
import os
import seaborn as sns
from funciones import actualizar_etiquetas_parametros, generar_numeros, crear_kde
from src.Generadores import *
from src.Distribuciones.Uniforme import generar_uniforme
from src.Distribuciones.Exponencial import generar_exponencial
from src.Distribuciones.Normal import generar_distribucion_normal
import pantalla

class SimuladorDistribucionesApp:
    def __init__(self):
        """Inicializa la aplicación y carga la pantalla principal."""
        self.root = tk.Tk()
        self.app = PantallaPrincipal(self.root)
        self.root.mainloop()

if __name__ == "__main__":
    SimuladorDistribucionesApp()