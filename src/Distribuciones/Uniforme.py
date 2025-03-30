def generar_uniforme(tamaño, a, b, generador=None):
    """
    Genera números aleatorios con distribución uniforme en el intervalo [a, b].
    
    Parámetros:
    - tamaño: cantidad de números a generar
    - a: límite inferior del intervalo
    - b: límite superior del intervalo
    - generador: instancia de GeneradorCongruencialLineal (opcional)
    
    Retorna:
    - Lista de números que siguen una distribución uniforme en [a, b]
    """
    # Si no se proporciona un generador, crear uno con parámetros predeterminados
    if generador is None:
        import sys
        import os

        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

        # Importar la clase GeneradorCongruencialLineal desde su ubicación
        from src.Generadores.GeneradorCongruencialLineal import GeneradorCongruencialLineal  # Updated import path
        generador = GeneradorCongruencialLineal(
            semilla=12345,
            a=1103515245,  # Parámetros para período máximo
            c=12345,
            m=2**31
        )
    
    # Transformación lineal de [0,1) a [a,b)
    numeros_uniformes = []
    for _ in range(tamaño):
        u = generador.siguiente()
        # Transformación lineal
        x = a + u * (b - a)
        numeros_uniformes.append(x)
    
    return numeros_uniformes