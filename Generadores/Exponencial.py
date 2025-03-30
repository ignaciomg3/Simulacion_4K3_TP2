import random
import math

def generar_exponencial(lam, n):
    """
    Genera una lista de números con distribución exponencial.

    Parámetros:
    lam (float): Tasa de la distribución (lambda > 0).
    n (int): Cantidad de números a generar.

    Retorna:
    list: Lista de números generados con distribución exponencial.
    """
    if lam <= 0:
        raise ValueError("El parámetro lambda debe ser mayor a 0.")
    if n <= 0:
        raise ValueError("La cantidad de números a generar debe ser mayor a 0.")
    
    return [-math.log(1 - random.random()) / lam for _ in range(n)]