class GeneradorCongruencialLineal:
    def __init__(self, semilla, a, c, m):
        """
        Inicializa el generador congruencial lineal.
        
        Parámetros:
        - semilla: valor inicial X_0
        - a: multiplicador
        - c: incremento
        - m: módulo
        """
        self.estado_actual = semilla
        self.a = a
        self.c = c
        self.m = m
        
        # Verificar si cumple condiciones para período máximo
        self.periodo_maximo = self.verificar_periodo_maximo()
    
    def verificar_periodo_maximo(self):
        """
        Verifica si los parámetros cumplen las condiciones para período máximo.
        Retorna True si cumple, False en caso contrario.
        """
        # Verificar si m es potencia de 2
        es_potencia_de_2 = (self.m & (self.m - 1) == 0) and self.m > 0
        
        if not es_potencia_de_2:
            print(f"Advertencia: m = {self.m} no es potencia de 2. No se garantiza período máximo.")
            return False
        
        # Verificar si a = 1 + 4k
        cumple_condicion_a = (self.a % 4 == 1)
        
        if not cumple_condicion_a:
            print(f"Advertencia: a = {self.a} no tiene la forma 1 + 4k. No se garantiza período máximo.")
            return False
        
        # Verificar si c es impar (relativamente primo a m cuando m es potencia de 2)
        es_c_impar = (self.c % 2 == 1)
        
        if not es_c_impar:
            print(f"Advertencia: c = {self.c} no es impar. No se garantiza período máximo.")
            return False
        
        print("Los parámetros cumplen las condiciones para período máximo.")
        return True
    
    def obtener_periodo_teorico(self):
        """
        Retorna el período teórico del generador según sus parámetros.
        """
        if self.periodo_maximo:
            return self.m
        else:
            # Si no cumple condiciones para período máximo, calculamos una estimación
            # Esta es una estimación aproximada y puede no ser precisa para todos los casos
            if self.c == 0:  # Si c=0, el período depende del MCD(m, semilla)
                import math
                return self.m // math.gcd(self.m, self.estado_actual)
            else:
                # Para otros casos, es difícil estimar sin análisis completo
                return "No determinado (< m)"
    
    def siguiente(self):
        """
        Genera el siguiente número pseudoaleatorio en la secuencia
        y devuelve un valor entre [0,1)
        """
        self.estado_actual = (self.a * self.estado_actual + self.c) % self.m
        return self.estado_actual / self.m
    
    def generar_secuencia(self, n):
        """
        Genera una secuencia de n números pseudoaleatorios
        """
        return [self.siguiente() for _ in range(n)]