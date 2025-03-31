import matplotlib.pyplot as plt
import numpy as np
from tkinter import messagebox

def actualizar_etiquetas_parametros(distribucion, lbl_param1, lbl_param2, entry_param2, param1, param2):
    """Actualiza las etiquetas de los parámetros según la distribución seleccionada"""
    if distribucion == "Uniforme":
        lbl_param1.configure(text="Límite inferior (a):")
        lbl_param2.configure(text="Límite superior (b):")
        entry_param2.configure(state="normal")
        param1.set("0")
        param2.set("1")

    elif distribucion == "Exponencial":
        lbl_param1.configure(text="Lambda (λ):")
        lbl_param2.configure(text="")
        entry_param2.configure(state="disabled")
        param1.set("1")
        param2.set("")

    elif distribucion == "Normal":
        lbl_param1.configure(text="Media (μ):")
        lbl_param2.configure(text="Desviación estándar (σ):")
        entry_param2.configure(state="normal")
        param1.set("0")
        param2.set("1")


def generar_numeros(cantidad, distribucion, param1, param2, generador):
    """Genera números aleatorios según la configuración seleccionada"""
    try:
        cantidad = int(cantidad)
        if not (0 < cantidad <= 1000000):
            raise ValueError("El tamaño de muestra debe ser mayor a 0 y menor o igual a 1,000,000")

        if distribucion == "Uniforme":
            a = float(param1)
            b = float(param2)
            if a >= b:
                raise ValueError("El límite inferior debe ser menor que el límite superior")

            numeros_generados = np.random.uniform(a, b, cantidad)
            titulo = f"Distribución Uniforme [{a}, {b}]"

        elif distribucion == "Exponencial":
            lambd = float(param1)
            if lambd <= 0:
                raise ValueError("Lambda debe ser mayor que 0")

            numeros_generados = np.random.exponential(1/lambd, cantidad)
            titulo = f"Distribución Exponencial (λ={lambd})"

        elif distribucion == "Normal":
            mu = float(param1)
            sigma = float(param2)
            if sigma <= 0:
                raise ValueError("La desviación estándar debe ser mayor que 0")

            numeros_generados = np.random.normal(mu, sigma, cantidad)
            titulo = f"Distribución Normal (μ={mu}, σ={sigma})"

        return numeros_generados, titulo

    except ValueError as e:
        messagebox.showerror("Error de entrada", str(e))
        return None, None
    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")
        return None, None


def crear_kde(ax, numeros_generados, titulo):
    """Genera un KDE en lugar de un histograma"""
    ax.clear()
    ax.hist(numeros_generados, bins=30, density=True, alpha=0.6, color='b')
    ax.set_title(titulo)
    ax.set_xlabel("Valor")
    ax.set_ylabel("Densidad")
    ax.figure.tight_layout()
