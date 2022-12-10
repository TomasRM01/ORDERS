import random

# Clase que representa un individuo (solución) en el algoritmo genético
class Individuo:
    def __init__(self, ruta):
        self.ruta = ruta
        self.distancia = calcular_distancia(ruta)
        
    def mutar(self):
        # Seleccionar dos posiciones aleatorias en la ruta y permutarlas
        i, j = random.sample(range(len(self.ruta)), 2)
        self.ruta[i], self.ruta[j] = self.ruta[j], self.ruta[i]
        self.distancia = calcular_distancia(self.ruta)

# Clase que representa una población de individuos en el algoritmo genético
class Poblacion:
    def __init__(self, coordenadas, tamano_poblacion=100, probabilidad_cruce=0.8, probabilidad_mutacion=0.1):
        self.coordenadas = coordenadas
        self.tamano_poblacion = tamano_poblacion
        self.probabilidad_cruce = probabilidad_cruce
        self.probabilidad_mutacion = probabilidad_mutacion
        self.individuos = [Individuo(generar_ruta_aleatoria(coordenadas)) for _ in range(tamano_poblacion)]
        
    def seleccionar(self):
        # Ordenar los individuos por distancia (menor a mayor)
        self.individuos.sort(key=lambda individuo: individuo.distancia)
        # Seleccionar los dos mejores individuos (padres) para el cruce
        padre1, padre2 = self.individuos[0], self.individuos[1]
        return padre1, padre2
    
    def cruzar(self, padre1, padre2):
        # Generar dos nuevos individuos (hijos) a partir del cruce de los padres
        hijo1 = [None] * len(padre1.ruta)
        hijo2 = [None] * len(padre1.ruta)
        inicio = random.randrange(len(padre1.ruta))
        fin = random.randrange(inicio, len(padre1.ruta))
        hijo1[inicio:fin] = padre1.ruta[inicio:fin]
        hijo2[inicio:fin] = padre2
