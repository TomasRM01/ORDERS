import math


# Funcion auxiliar que calcula la distancia euclidea entre dos puntos
def distanciaEuclidea(punto1, punto2):
    x1, y1 = punto1
    x2, y2 = punto2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


# Funcion auxiliar que calcula la distancia total recorrida por un dron
def distanciaTotalDron(caminoDron):
    distancia = 0
    for i in range(len(caminoDron) - 1):
        distancia += distanciaEuclidea(caminoDron[i][0], caminoDron[i + 1][0])
    distancia += distanciaEuclidea(caminoDron[-1][0], caminoDron[0][0])
    return distancia


# Funcion auxiliar que calcula la bateria total recargada por un dron
def bateriaTotalDron(caminoDron):
    bateria = 0
    for sensor in caminoDron:
        bateria += sensor[2]
    return bateria


# Funcion auxiliar que calcula la prioridad total recorrida por un dron
def prioridadTotalDron(caminoDron):
    prioridad = 0
    for sensor in caminoDron:
        prioridad += sensor[1]
    return prioridad