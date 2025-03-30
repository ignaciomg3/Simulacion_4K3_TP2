import random

class Fila:
    def __init__(self, hora, hora_fin, estado1, estado2, estado3):
        self.hora = hora
        self.hora_fin = hora_fin
        self.estado1 = estado1
        self.estado2 = estado2
        self.estado3 = estado3

    def __repr__(self):
        return f"Fila(Hora={self.hora}, HoraFin={self.hora_fin}, Estado1={self.estado1}, Estado2={self.estado2}, Estado3={self.estado3})"

    @staticmethod
    def generar_filas(cantidad):
        filas = []
        for i in range(cantidad):
            hora = f"{8 + i}:00"
            hora_fin = f"{9 + i}:00"
            estado1 = random.choice(["Activo", "Inactivo"])
            estado2 = random.choice(["Ocupado", "Libre"])
            estado3 = random.choice(["En espera", "En proceso"])
            filas.append(Fila(hora, hora_fin, estado1, estado2, estado3))
        return filas
