import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sys
import os

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
        self.root.geometry("1200x800")
        
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
        frame_config = ttk.LabelFrame(self.root, text="Configuración")
        frame_config.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        
        # Selector de distribución
        ttk.Label(frame_config, text="Distribución:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        distribuciones = ["Uniforme", "Exponencial", "Normal"]
        combo_dist = ttk.Combobox(frame_config, textvariable=self.distribucion_seleccionada, 
                                  values=distribuciones, state="readonly")
        combo_dist.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        combo_dist.bind("<<ComboboxSelected>>", self.actualizar_etiquetas_parametros)
        
        # Cantidad de números
        ttk.Label(frame_config, text="Tamaño de muestra:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_config, textvariable=self.cantidad_numeros).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Número de intervalos para histograma
        ttk.Label(frame_config, text="Número de intervalos:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        intervalos = ["10", "15", "20", "30"]
        ttk.Combobox(frame_config, textvariable=self.num_intervalos, 
                     values=intervalos, state="readonly").grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        # Parámetros (etiquetas se actualizarán según la distribución)
        self.lbl_param1 = ttk.Label(frame_config, text="Parámetro 1:")
        self.lbl_param1.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_config, textvariable=self.param1).grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        self.lbl_param2 = ttk.Label(frame_config, text="Parámetro 2:")
        self.lbl_param2.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_param2 = ttk.Entry(frame_config, textvariable=self.param2)
        self.entry_param2.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        
        # Botón para generar
        ttk.Button(frame_config, text="Generar Números", 
                   command=self.generar_numeros).grid(row=5, column=0, columnspan=2, padx=5, pady=10)
    
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
            
            # Generar histograma y tabla
            self.crear_histograma(titulo)
            self.crear_tabla_frecuencias()
            
        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")
    
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
        total = len(self.numeros_generados)
        frecuencias_relativas = [f/total for f in frecuencias]
        
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

    def export_to_excel(self):
        data = []
        for item in self.tree.get_children():
            data.append(self.tree.item(item)['values'])
        
        df = pd.DataFrame(data, columns=["Hora", "HoraFin", "Estado1", "Estado2", "Estado3"])
        
        try:
            df.to_excel("datos.xlsx", index=False)
            messagebox.showinfo("Éxito", "Datos exportados a datos.xlsx")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorDistribucionesApp(root)
    root.mainloop()