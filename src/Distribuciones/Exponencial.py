import math

def generar_exponencial(tamaño, lambd, generador=None):
    """
    Genera números aleatorios con distribución exponencial.
    
    Parámetros:
    - tamaño: cantidad de números a generar
    - lambd: parámetro lambda de la distribución (tasa)
    - generador: instancia de GeneradorCongruencialLineal (opcional)
    
    Retorna:
    - Lista de números que siguen una distribución exponencial
    """
    # Si no se proporciona un generador, crear uno con parámetros predeterminados
    if generador is None:
        from ..Generadores.GeneradorCongruencialLineal import GeneradorCongruencialLineal
        generador = GeneradorCongruencialLineal(
            semilla=12345,
            a=1103515245,  # Parámetros para período máximo
            c=12345,
            m=2**31
        )
    
    # Aplicar el método de la transformada inversa
    numeros_exponenciales = []
    for _ in range(tamaño):
        u = generador.siguiente()
        # Evitar logaritmo de 0
        if u == 1.0:
            u = 0.9999999999
        # Fórmula de la transformada inversa para exponencial
        x = -math.log(1.0 - u) / lambd
        numeros_exponenciales.append(round(x, 4))
    
    return numeros_exponenciales