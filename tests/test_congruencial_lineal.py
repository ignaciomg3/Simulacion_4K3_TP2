import unittest
import math
import statistics
from src.Distribuciones.Uniforme import generar_uniforme
from src.Distribuciones.Exponencial import generar_exponencial
from src.Distribuciones.Normal import generar_distribucion_normal
from src.Generadores.GeneradorCongruencialLineal import GeneradorCongruencialLineal


class TestGeneradorCongruencialLineal(unittest.TestCase):
    
    def test_formula_basica(self):
        """Prueba que la implementación de la fórmula sea correcta"""
        # Parámetros sencillos para validar manualmente
        gcl = GeneradorCongruencialLineal(semilla=5, a=7, c=3, m=11)
        
        # Valores esperados calculados manualmente:
        # X₁ = (7*5 + 3) % 11 = 38 % 11 = 5
        # X₂ = (7*5 + 3) % 11 = 38 % 11 = 5
        # X₃ = (7*5 + 3) % 11 = 38 % 11 = 5
        
        self.assertEqual(gcl.siguiente() * 11, 5)
        self.assertEqual(gcl.siguiente() * 11, 5)
        self.assertEqual(gcl.siguiente() * 11, 5)
    
    def test_periodo_completo(self):
        """Prueba que un generador con parámetros para período máximo recorra todos los valores"""
        # Usamos parámetros para período máximo con m pequeño para la prueba
        m = 16  # 2^4
        gcl = GeneradorCongruencialLineal(semilla=7, a=5, c=3, m=m)
        
        # Generamos m números y verificamos que todos sean diferentes
        valores = set()
        for _ in range(m):
            valores.add(int(gcl.siguiente() * m))
        
        # Verificamos que hayamos generado todos los valores posibles
        self.assertEqual(len(valores), m)
        self.assertEqual(valores, set(range(m)))
    
    def test_periodo_no_maximo(self):
        """Prueba un generador que no cumple condiciones para período máximo"""
        # a no cumple la forma 1+4k
        gcl = GeneradorCongruencialLineal(semilla=3, a=6, c=3, m=16)
        
        # Contamos cuántos valores diferentes generamos antes de repetir
        valores = []
        vistos = set()
        
        # Generamos hasta encontrar repetición o llegar a m iteraciones
        for _ in range(16):
            valor = int(gcl.siguiente() * 16)
            valores.append(valor)
            if valor in vistos:
                break
            vistos.add(valor)
        
        # Verificamos que el período sea menor que m
        self.assertLess(len(vistos), 16)
    
    def test_uniformidad_basica(self):
        """Prueba que los números generados estén uniformemente distribuidos"""
        # Parámetros para período máximo
        gcl = GeneradorCongruencialLineal(semilla=12345, a=21, c=3, m=2**16)
        
        # Generamos una muestra grande
        n = 10000
        numeros = gcl.generar_secuencia(n)
        
        # Verificamos que el promedio sea cercano a 0.5
        promedio = sum(numeros) / n
        self.assertAlmostEqual(promedio, 0.5, delta=0.05)
        
        # Verificamos que el mínimo y máximo estén cerca de 0 y 1
        self.assertLess(min(numeros), 0.05)
        self.assertGreater(max(numeros), 0.95)
    
    def test_distribuciones(self):
        """Prueba que las distribuciones generadas tengan propiedades básicas esperadas"""
        # Creamos generador con período máximo
        gcl = GeneradorCongruencialLineal(semilla=12345, a=21, c=3, m=2**16)
        
        # Probamos distribución uniforme
        n = 5000
        a, b = 10, 20
        uniforme = generar_uniforme(n, a, b)
        
        # Verificamos propiedades básicas de distribución uniforme
        self.assertAlmostEqual(statistics.mean(uniforme), (a + b) / 2, delta=0.5)
        self.assertGreaterEqual(min(uniforme), a - 0.01)
        self.assertLessEqual(max(uniforme), b + 0.01)
        
        # Probamos distribución exponencial con lambda=0.5
        lambd = 0.5
        exponencial = generar_exponencial(n, lambd)
        
        # Verificamos propiedades básicas de distribución exponencial
        self.assertAlmostEqual(statistics.mean(exponencial), 1/lambd, delta=0.5)
        self.assertGreaterEqual(min(exponencial), 0)
        
        # Probamos distribución normal
        mu, sigma = 5, 2
        normal = generar_distribucion_normal(n, mu, sigma)
        
        # Verificamos propiedades básicas de distribución normal
        self.assertAlmostEqual(statistics.mean(normal), mu, delta=0.3)
        self.assertAlmostEqual(statistics.stdev(normal), sigma, delta=0.3)

if __name__ == '__main__':
    unittest.main()