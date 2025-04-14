import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
import sys
import os
import seaborn as sns
# Estas funciones no se usan
from funciones import actualizar_etiquetas_parametros, generar_numeros, crear_kde

# Añadir ruta del proyecto al PYTHONPATH para importaciones
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Importar los generadores
from src.Generadores.GeneradorCongruencialLineal import GeneradorCongruencialLineal
from src.Distribuciones.Uniforme import generar_uniforme
from src.Distribuciones.Exponencial import generar_exponencial
from src.Distribuciones.Normal import generar_distribucion_normal

class SimuladorDistribucionesApp:
    def __init__(self, root):
        self.root = root    
        self.root.title("Simulador de Distribuciones Aleatorias")
        self.root.geometry("1400x800")

        # Maximizar la ventana al iniciar
        self.root.state('zoomed')

        # Ajustar las columnas y filas de la ventana
        self.root.grid_columnconfigure(0, weight=2)  # Primera columna más grande
        self.root.grid_columnconfigure(1, weight=3)  # Segunda columna más grande
        self.root.grid_rowconfigure(0, weight=2)     # Primera fila más grande
        self.root.grid_rowconfigure(1, weight=2)     # Segunda fila más grande
        
        # Variables para almacenar la configuración
        self.distribucion_seleccionada = tk.StringVar(value="Uniforme")
        self.cantidad_numeros = tk.StringVar(value="1000")
        self.num_intervalos = tk.StringVar(value="10")
        self.param1 = tk.StringVar(value="0")
        self.param2 = tk.StringVar(value="1")
        
        # Variables para almacenar resultados
        self.numeros_generados = []
        
        # Crear el generador congruencial lineal
        self.generador = GeneradorCongruencialLineal(
            semilla=12345,
            a=1103515245,
            c=12345,
            m=2**31
        )
        
        # Crear frames
        self.crear_frame_configuracion()
        self.crear_frame_grafico()
        self.crear_frame_tabla()

        
        
        # Actualizar etiquetas de parámetros según distribución inicial
        self.actualizar_etiquetas_parametros()
        
    def crear_frame_configuracion(self):
        """Crea el panel de configuración para seleccionar distribuciones y parámetros"""
        frame_config = ttk.LabelFrame(self.root, text="Configuración", width=900, height=600)  # Tamaño inicial del frame
        frame_config.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        
        # Configurar el layout para que el frame ocupe más espacio
        self.root.grid_columnconfigure(0, weight=1)  # Asegura que la columna de la izquierda sea flexible
        self.root.grid_rowconfigure(0, weight=1)     # Asegura que la fila de arriba sea flexible
        
        frame_config.grid_columnconfigure(0, weight=1, minsize=200)  # Aumentar el tamaño de la columna 0
        frame_config.grid_columnconfigure(1, weight=2, minsize=400)  # Aumentar el tamaño de la columna 1
        
        # Selector de distribución
        ttk.Label(frame_config, text="Distribución:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        distribuciones = ["Uniforme", "Exponencial", "Normal"]
        combo_dist = ttk.Combobox(frame_config, textvariable=self.distribucion_seleccionada, 
                                values=distribuciones, state="readonly", font=("Arial", 12))
        combo_dist.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        combo_dist.bind("<<ComboboxSelected>>", self.actualizar_etiquetas_parametros)
        
        # Cantidad de números
        ttk.Label(frame_config, text="Tamaño de muestra:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        ttk.Entry(frame_config, textvariable=self.cantidad_numeros, font=("Arial", 12)).grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Número de intervalos para histograma
        ttk.Label(frame_config, text="Número de intervalos:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        intervalos = ["10", "15", "20", "30"]
        ttk.Combobox(frame_config, textvariable=self.num_intervalos, 
                    values=intervalos, state="readonly", font=("Arial", 12)).grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        # Parámetros (etiquetas se actualizarán según la distribución)
        self.lbl_param1 = ttk.Label(frame_config, text="Parámetro 1:", font=("Arial", 12))
        self.lbl_param1.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        ttk.Entry(frame_config, textvariable=self.param1, font=("Arial", 12)).grid(row=3, column=1, padx=10, pady=10, sticky="w")
        
        self.lbl_param2 = ttk.Label(frame_config, text="Parámetro 2:", font=("Arial", 12))
        self.lbl_param2.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.entry_param2 = ttk.Entry(frame_config, textvariable=self.param2, font=("Arial", 12))
        self.entry_param2.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        
        #defino estilo 
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 14), padding=(10, 10), background="#90EE90")  # Aumenta el padding y establece color verde claro

        # Botón para generar
        ttk.Button(frame_config, text="Generar Números", 
                command=self.generar_numeros).grid(row=5, column=1, padx=(10, 20), pady=10, sticky="e")
        
        # Botón para exportar frecuencias
        self.btn_export = ttk.Button(frame_config, text="Exportar frecuencias", command=self.export_frequency_to_excel, width=20, style="TButton")
        self.btn_export.grid(row=5, column=0, padx=(20, 5), pady=10, sticky="w")
        
        # Botón para exportar serie de números
        self.btn_export = ttk.Button(frame_config, text="Exportar números", command=self.export_numbers_to_excel, width=20, style="TButton")
        self.btn_export.grid(row=6, column=0, padx=(20, 5), pady=10, sticky="w")
        
        # Botón para abrir ventana con números
        ttk.Button(frame_config, text="Mostrar Números", 
                command=self.mostrar_numeros_generados, width=20, style="TButton").grid(row=6, column=1, padx=(10, 20), pady=5, sticky="e")


    def crear_frame_grafico(self):
        """Crea el panel para mostrar el histograma"""
        frame_grafico = ttk.LabelFrame(self.root, text="Histograma")
        frame_grafico.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")
        
        # Crear figura de matplotlib
        self.fig, self.ax = plt.subplots(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_grafico)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Configurar gráfico inicial
        self.ax.set_title("Histograma de Frecuencias")
        self.ax.set_xlabel("Valor")
        self.ax.set_ylabel("Frecuencia")
        self.fig.tight_layout()
    

    def crear_frame_tabla(self):
        """Crea el panel para mostrar la tabla de frecuencias"""
        frame_tabla = ttk.LabelFrame(self.root, text="Tabla de Frecuencias")
        frame_tabla.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Crear Treeview para la tabla
        columnas = ("Intervalo", "Límite Inferior", "Límite Superior", "Frecuencia", "Frecuencia Relativa")
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)
        
        # Configurar encabezados y anchos
        for idx, col in enumerate(columnas):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Añadir scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar elementos
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    

    def actualizar_etiquetas_parametros(self, event=None):
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
    

    def generar_numeros(self):
        """Genera números aleatorios según la configuración seleccionada"""
        try:
            # Validar parámetros
            cantidad = int(self.cantidad_numeros.get())
            if not (0 < cantidad <= 1000000):
                raise ValueError("El tamaño de muestra debe ser mayor a 0 y menor o igual a 1,000,000")
            
            distribucion = self.distribucion_seleccionada.get()
            
            if distribucion == "Uniforme":
                a = float(self.param1.get())
                b = float(self.param2.get())
                if a >= b:
                    raise ValueError("El límite inferior debe ser menor que el límite superior")
                
                self.numeros_generados = generar_uniforme(cantidad, a, b, self.generador)
                titulo = f"Distribución Uniforme [{a}, {b}]"
            
            elif distribucion == "Exponencial":
                lambd = float(self.param1.get())
                if lambd <= 0:
                    raise ValueError("Lambda debe ser mayor que 0")
                
                self.numeros_generados = generar_exponencial(cantidad, lambd, self.generador)
                titulo = f"Distribución Exponencial (λ={lambd})"
            
            elif distribucion == "Normal":
                mu = float(self.param1.get())
                sigma = float(self.param2.get())
                if sigma <= 0:
                    raise ValueError("La desviación estándar debe ser mayor que 0")
                
                self.numeros_generados = generar_distribucion_normal(cantidad, mu, sigma, self.generador)
                titulo = f"Distribución Normal (μ={mu}, σ={sigma})"
            
            self.crear_histograma(titulo)
            self.crear_tabla_frecuencias()
        
        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")
    

    def mostrar_numeros_generados(self):
        """Crea una nueva ventana para mostrar todos los números generados en columnas"""
        # Crear una nueva ventana
        ventana_numeros = tk.Toplevel(self.root)
        ventana_numeros.title("Números Generados")
        ventana_numeros.geometry("400x600")
    
        # Crear un Treeview para mostrar los números en columnas
        columnas = ("Índice", "Número")
        tree = ttk.Treeview(ventana_numeros, columns=columnas, show="headings", height=25)
    
        # Configurar encabezados y anchos de columnas
        tree.heading("Índice", text="Índice")
        tree.heading("Número", text="Número")
        tree.column("Índice", width=20, anchor="center")
        tree.column("Número", width=120, anchor="center")
    
        # Llenar el Treeview con los números generados
        for i, numero in enumerate(self.numeros_generados, start=1):
            tree.insert("", "end", values=(i, f"{numero:.4f}"))
    
        # Añadir un scrollbar vertical
        scrollbar = ttk.Scrollbar(ventana_numeros, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
    
        # Posicionar el Treeview y el scrollbar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    

    def crear_histograma(self, titulo):
        """Crea el histograma con los números generados"""
        # Limpiar gráfico anterior
        self.ax.clear()
        
        # Obtener número de intervalos
        num_intervalos = int(self.num_intervalos.get())
        
        # Crear histograma
        n, bins, patches = self.ax.hist(self.numeros_generados, bins=num_intervalos, 
                                        edgecolor='black', alpha=0.7)
        
        # Calcular frecuencia máxima para escala Y
        max_freq = max(n) * 1.1
        
        # Configurar etiquetas y título
        self.ax.set_xlabel("Valor")
        self.ax.set_ylabel("Frecuencia")
        self.ax.set_title(f"Histograma de {titulo}\n({len(self.numeros_generados)} números, {num_intervalos} intervalos)")
        self.ax.set_ylim(0, max_freq)
        
        # Añadir cuadrícula
        self.ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Aplicar cambios
        self.fig.tight_layout()
        self.canvas.draw()
    

    def crear_tabla_frecuencias(self):
        """Genera la tabla de frecuencias basada en el histograma"""
        # Limpiar tabla anterior
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obtener número de intervalos
        num_intervalos = int(self.num_intervalos.get())

        # Calcular límites de intervalos
        min_val = min(self.numeros_generados)
        max_val = max(self.numeros_generados)
        ancho = (max_val - min_val) / num_intervalos

        # Contar frecuencias
        frecuencias = [0] * num_intervalos
        for num in self.numeros_generados:
            idx = min(int((num - min_val) / ancho), num_intervalos - 1)
            frecuencias[idx] += 1

        # Calcular frecuencias relativas
        total = sum(frecuencias)  # Debería ser igual a len(self.numeros_generados)
        frecuencias_relativas = [f/total for f in frecuencias]

        # Verificar que la suma de frecuencias relativas sea 1
        suma_freq_rel = sum(frecuencias_relativas)
        print(f"Suma de frecuencias relativas: {suma_freq_rel}")  # Debería ser aproximadamente 1.0

        # Llenar tabla
        for i in range(num_intervalos):
            limite_inf = min_val + i * ancho
            limite_sup = min_val + (i + 1) * ancho
            
            # Para el último intervalo, asegurarse de incluir el valor máximo
            if i == num_intervalos - 1:
                limite_sup = max_val
            
            self.tree.insert("", "end", values=(
                f"Intervalo {i+1}",
                f"{limite_inf:.4f}",
                f"{limite_sup:.4f}",
                frecuencias[i],
                f"{frecuencias_relativas[i]:.4f}"
            ))


    def export_frequency_to_excel(self):
        data = []
        for item in self.tree.get_children():
            data.append(self.tree.item(item)['values'])
        
        df = pd.DataFrame(data, columns=["Intervalo", "Límite Inferior", "Límite Superior", "Frecuencia", "Frecuencia Relativa"])
        
        try:
            df.to_excel("datos.xlsx", index=False)
            messagebox.showinfo("Éxito", "Datos exportados a datos.xlsx")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {e}")


    def export_numbers_to_excel(self):
        """Exporta los números generados a un archivo Excel"""
        try:
            # Crear un DataFrame con los números generados
            data = {"Índice": range(1, len(self.numeros_generados) + 1), 
                    "Número": [f"{num:.4f}" for num in self.numeros_generados]}
            df = pd.DataFrame(data)
    
            # Exportar a un archivo Excel
            df.to_excel("numeros_generados.xlsx", index=False)
            messagebox.showinfo("Éxito", "Números exportados a numeros_generados.xlsx")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorDistribucionesApp(root)

    # Funcion para terminar el programa al cerrar la ventana
    def on_closing():
        if messagebox.askokcancel("Salir", "¿Estás seguro de que deseas cerrar la aplicación?"):
            root.destroy()  # Close the Tkinter window
            sys.exit()  # Ensure the program terminates completely

    # Ejecuta on_closing al cerrar la ventana
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()