import numpy as np

def generar_distribucion_normal(media, desviacion_estandar, cantidad):
    """
    Genera una distribución normal de números.

    :param media: Media de la distribución
    :param desviacion_estandar: Desviación estándar de la distribución
    :param cantidad: Cantidad de números a generar
    :return: Lista de números generados
    """
    return np.random.normal(loc=media, scale=desviacion_estandar, size=cantidad)

# Ejemplo de uso
if __name__ == "__main__":
    media = 0
    desviacion_estandar = 1
    cantidad = 1000

    numeros = generar_distribucion_normal(media, desviacion_estandar, cantidad)
    print(numeros)