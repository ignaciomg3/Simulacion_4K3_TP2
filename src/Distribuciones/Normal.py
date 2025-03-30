import math

def generar_distribucion_normal(tamaño, mu, sigma, generador=None):
    """
    Genera números aleatorios con distribución normal.
    
    Parámetros:
    - tamaño: cantidad de números a generar
    - mu: media de la distribución
    - sigma: desviación estándar de la distribución
    - generador: instancia de GeneradorCongruencialLineal (opcional)
    
    Retorna:
    - Lista de números que siguen una distribución normal
    """
    # Si no se proporciona un generador, crear uno con parámetros predeterminados
    if generador is None:
        import sys
        import os
        
        # Añadir la raíz del proyecto al path
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
        
        # Importar el generador
        from src.Generadores.GeneradorCongruencialLineal import GeneradorCongruencialLineal
        
        generador = GeneradorCongruencialLineal(
            semilla=12345,
            a=1103515245,
            c=12345,
            m=2**31
        )
    
    # Implementar el método de Box-Muller para generar variables aleatorias normales
    numeros_normales = []
    for _ in range((tamaño + 1) // 2):  # Generamos pares de números
        u1 = generador.siguiente()
        u2 = generador.siguiente()
        
        # Transformación de Box-Muller
        z1 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
        z2 = math.sqrt(-2.0 * math.log(u1)) * math.sin(2.0 * math.pi * u2)
        
        # Transformar a la media y desviación estándar deseadas
        numeros_normales.append(mu + sigma * z1)
        if len(numeros_normales) < tamaño:  # Para manejar tamaños impares
            numeros_normales.append(mu + sigma * z2)
    
    return numeros_normales[:tamaño]  # Aseguramos que devolvemos exactamente tamaño elementos