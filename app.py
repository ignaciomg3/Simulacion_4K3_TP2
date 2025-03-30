from Entidades import Fila  # Importamos la clase Fila
from Entidades.Fila import Fila  # Importamos la clase Fila
import tkinter as tk
from tkinter import ttk


class SimulacionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación")

        # Input para el número de simulaciones
        tk.Label(root, text="Número de simulaciones:").grid(row=0, column=0, padx=5, pady=5)
        self.num_simulaciones = tk.Entry(root)
        self.num_simulaciones.grid(row=0, column=1, padx=5, pady=5)

        # Botón para crear simulación
        self.btn_crear = tk.Button(root, text="Crear Simulación", command=self.crear_simulacion)
        self.btn_crear.grid(row=0, column=2, padx=5, pady=5)

        # Tabla (Treeview) para mostrar la grilla
        columnas = ("Hora", "HoraFin", "Estado1", "Estado2", "Estado3")
        self.tree = ttk.Treeview(root, columns=columnas, show="headings")

        # Configurar encabezados de la tabla
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

    def crear_simulacion(self):
        # Limpiar la tabla antes de agregar nuevas filas
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obtener el número de simulaciones ingresado
        try:
            cantidad = int(self.num_simulaciones.get())
            if cantidad <= 0:
                raise ValueError("El número debe ser mayor a 0")
        except ValueError:
            print("Ingrese un número válido")
            return

        # Generar filas y agregarlas a la tabla
        filas = Fila.generar_filas(cantidad)
        for fila in filas:
            self.tree.insert("", "end", values=(fila.hora, fila.hora_fin, fila.estado1, fila.estado2, fila.estado3))

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulacionApp(root)
    root.mainloop()
