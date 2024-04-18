# Programa que resuelve el problema de los drones de sensores mediante algoritmos genéticos

# importamos librerias
import copy
import re
import random
import math
import time
import colorsys
import matplotlib.pyplot as plt
from random import randint


# Funcion main que ejecuta el algoritmo genetico para el problema de los drones y sensores
def main():
    
    # Variables importantes configurables para el algoritmo genetico
    peso_distancia = 0.001
    tamano_poblacion = 200
    porcentaje_mejor = 10
    probabilidad_mutante = 50
    maximo_generaciones_sin_mejora = 10
    
    # Recuperamos los drones del .txt
    drones = recuperaDrones()
        
    # Recuperamos los sensores del .txt
    listaSensores = recuperaSensores()
    
    # Arrancamos el cronometro
    inicio = time.time()
    
    # Llamamos al algoritmo genetico
    mejorSolucion = genetico(listaSensores, tamano_poblacion, porcentaje_mejor, probabilidad_mutante, maximo_generaciones_sin_mejora, drones, peso_distancia)

    # Paramos el cronometro y medimos el tiempo total
    fin = time.time()
    tiempo_total = fin - inicio
    
    # Escribimos los resultados obtenidos por el algoritmo genetico en un fichero de log
    escribirResultados(mejorSolucion, tamano_poblacion, porcentaje_mejor, probabilidad_mutante, maximo_generaciones_sin_mejora, tiempo_total, drones, peso_distancia, listaSensores)

    # Imprimimos la mejor solucion con una grafica
    dibujarCaminos(mejorSolucion, listaSensores, drones)


# Funcion que lee el contenido de el fichero scenary_drones.txt y devuelve la lista de drones con sus capacidades
def recuperaDrones():
    # lista de drones
    drones = []

    # abrimos el fichero en modo lectura
    with open("Escenario/scenary_drones.txt", "r") as f:
        # pasamos el contenido a un string
        s = f.read()
        
    # recuperamos los elementos del string tal que asi: {'distance_capacity': 137, 'battery_capacity': 1158}, {'distance_capacity': 108, 'battery_capacity': 1690}, ...
    drones = [eval(drone) for drone in re.findall(r'\{.*?\}', s)]

    # cerramos el fichero
    f.close()
    
    return drones

  
# Funcion que lee el contenido de el fichero scenary_sensores.txt y devuelve la lista de sensores con sus coordenadas
def recuperaSensores():
    
    # lista de sensores
    sensores = []

    # abrimos el fichero en modo lectura
    with open("Escenario/scenary_sensores.txt", "r") as f:
        # pasamos el contenido a un string
        s = f.read()

    # desechamos todo lo que no son numeros y lo convertimos en una lista de elementos
    s = [float(s) for s in re.findall(r'\d+\.?\d*', s)]

    # guardamos los elementos en las listas correspondientes
    contador = 0
    for i in range(0, len(s), 4):
        x = s[i]
        y = s[i+1]
        p = s[i+2]
        b = s[i+3]
        sensores.append(((x, y), p, b))

    return sensores


# Funcion que genera una solucion válida para el problema de los drones y sensores
# Rellena una listaDrones con sensores, de forma que se cumplan las restricciones de los drones
def generaSolucion(listaSensores, drones):
    
    # lista vacia de caminos para cada dron
    listaDrones = []
    for n in range(len(drones)):
        listaDrones.append([])
    
    # copia de la lista de sensores
    copiaListaSensores = copy.deepcopy(listaSensores)
    
    # obtenemos sensor inicial y lo eliminamos de la lista de sensores
    # despues, actualizamos prioridad y bateria del sensor inicial a 0
    sensorInicial = copiaListaSensores.pop(0)
    sensorInicial = (sensorInicial[0], 0, 0)
    
    # generamos un camino para cada dron
    for dron in drones:
        
        # inicializamos con la bateria y distancia restante del dron
        bateria = dron['battery_capacity']
        distancia = dron['distance_capacity']
        
        # incluimos el sensor inicial en el camino del dron
        listaDrones[drones.index(dron)].append(sensorInicial)
        
        # inicializamos el ultimo sensor con el sensor inicial
        ultimoSensor = sensorInicial
        
        # por cada sensor en la lista de sensores (en sentido inverso para poder eliminar sensores de la lista mientras la recorremos)
        for sensor in reversed(copiaListaSensores):
            
            # calculamos la distancia euclidea entre el ultimo sensor visitado y el sensor seleccionado
            distanciaSensor = distanciaEuclidea(ultimoSensor[0], sensor[0])
            
            # sumamos la distancia entre el sensor seleccionado y el sensor inicial
            distanciaSensorVuelta = distanciaSensor + distanciaEuclidea(sensor[0], sensorInicial[0])
            
            # si la bateria y la distancia restante del dron son suficientes para visitar el sensor seleccionado
            if bateria - sensor[2] > 0 and distancia - distanciaSensorVuelta > 0:
                
                bateria -= sensor[2]
                distancia -= distanciaSensor
                
                # incluimos el sensor seleccionado en el camino del dron
                listaDrones[drones.index(dron)].append(sensor)
                copiaListaSensores.remove(sensor)
                
                # actualizamos el ultimo sensor visitado
                ultimoSensor = sensor

    # devolvemos una lista de sensores visitados para cada dron
    return listaDrones


# Funcion que corrige una solucion incorrecta, haciendola válida usando una lista de sensores general
# Devuelve una lista que contiene N listas con caminos validos
def corrigeSolucion(listaDrones, listaSensores, drones): 

    # Hacemos una copia de las listas para no modificarlas
    copiaListaDrones = copy.deepcopy(listaDrones)
    copialistaSensores = copy.deepcopy(listaSensores)
    
    # Obtenemos el sensor inicial de la lista de sensores
    sensorInicial = (copialistaSensores[0][0], 0, 0)
    
    # eliminamos el sensor con las mismas coordenadas que el sensor de origen de la lista de sensores
    for sensor in reversed(copialistaSensores):
        if sensor[0] == sensorInicial[0]:
            copialistaSensores.remove(sensor)
            break
    
    # Creamos un contador para los sensores (diccionario vacio)
    contadorSensores = {}

    # Primero, obtenemos los sensores repetidos en la lista de drones
    for dron in copiaListaDrones:
        for sensor in dron:
            if sensor in contadorSensores:
                contadorSensores[sensor] += 1
            else:
                contadorSensores[sensor] = 1
                
    # Eliminar elementos que se repitan más de una vez
    for dron in copiaListaDrones:
        # Recorremos la lista en sentido inverso
        for sensor in reversed(dron):
            # Si el sensor está repetido o tiene las mismas coordenadas que el sensor de origen
            if contadorSensores[sensor] > 1 or sensor[0] == sensorInicial[0]: 
                # lo eliminamos de la lista
                dron.remove(sensor)
        
    # Una vez eliminados los sensores repetidos, comprobamos que no se superen las capacidades de los drones
    for dron in copiaListaDrones:
        # insertamos el sensor de origen al principio de la lista
        dron.insert(0, sensorInicial)
        # calculamos la distancia total recorrida y la bateria recargada por el dron
        distancia = distanciaTotalDron(dron)
        bateria = bateriaTotalDron(dron)
        
        # si la distancia supera la capacidad del dron, eliminamos sensores aleatorios hasta que se cumplan las condiciones
        while distancia > drones[copiaListaDrones.index(dron)].get('distance_capacity') or bateria > drones[copiaListaDrones.index(dron)].get('battery_capacity'):
            # seleccionamos un sensor aleatorio para eliminar del camino del dron (menos el sensor de origen)
            sensor = random.choice(dron[1:])
            # eliminamos el sensor del camino del dron
            dron.remove(sensor)
            # recalculamos la distancia total recorrida y la bateria recargada por el dron
            distancia = distanciaTotalDron(dron)
            bateria = bateriaTotalDron(dron)
    
    # Obtenemos la lista de sensores no visitados por ningun dron
    sensoresNoVisitados = []
    for sensor in copialistaSensores:
        visitado = False
        for dron in copiaListaDrones:
            if sensor in dron:
                visitado = True
                break
        if not visitado:
            sensoresNoVisitados.append(sensor)
    
    # por cada sensor no visitado, intentamos insertarlo en un dron aleatorio
    for sensor in reversed(sensoresNoVisitados):
        # seleccionamos un dron aleatorio
        dron = random.choice(copiaListaDrones)
        # insertamos el sensor en una posición aleatoria del dron
        dron.insert(randint(1, len(dron)), sensor)
        # calculamos la distancia total recorrida y la bateria recargada por el dron
        distancia = distanciaTotalDron(dron)
        bateria = bateriaTotalDron(dron)
        # si la distancia supera la capacidad del dron, eliminamos el sensor
        if distancia > drones[copiaListaDrones.index(dron)].get('distance_capacity') or bateria > drones[copiaListaDrones.index(dron)].get('battery_capacity'):
            dron.remove(sensor)
        else:
            # si el sensor se ha insertado correctamente, lo eliminamos de la lista de sensores no visitados
            sensoresNoVisitados.remove(sensor)
    
    # Devolver los vectores como una tupla
    return copiaListaDrones


# Funcion que recibe una posible solución, calcula las distancias y las prioridades de los drones y devuelve el fitness de la solución
def fitness(listaDrones, peso_distancia):

    # inicializamos variables
    f = 0.0
    distancia = 0
    prioridad = 0

    # calculamos la distancia y prioridad total
    for dron in listaDrones:
        distancia += distanciaTotalDron(dron)
        prioridad += prioridadTotalDron(dron)
            
    # la funcion de fitness es la prioridad menos la distancia por el peso de la distancia
    f = (prioridad - (peso_distancia * distancia))

    # devolvemos el fitness de la solución
    return f


# Funcion que recibe dos soluciones correctas y las combina, creando dos nuevas soluciones. Estas soluciones NO son correctas, es decir, hay que 
# corregirlas con la función corrigeSolucion
def combinarSoluciones(listaDronesPadre, listaDronesMadre):

    # Creamos dos listas vacias para devolver las posibles soluciones
    listaDronesHijo1 = []
    listaDronesHijo2 = []
    
    # para cada dron de las dos soluciones
    for dronPadre, dronMadre in zip(listaDronesPadre, listaDronesMadre):

        # calculamos los puntos medios de los vectores
        if len(dronPadre) == 1:
            puntoMedioPadre = 0
        else:
            puntoMedioPadre = len(dronPadre) // random.randint(1, len(dronPadre) - 1)

        if len(dronMadre) == 1:
            puntoMedioMadre = 0
        else:
            puntoMedioMadre = len(dronMadre) // random.randint(1, len(dronMadre) - 1)
        
        # combinamos los caminos creando dos nuevos caminos
        viajanteHijo1 = dronPadre[:puntoMedioPadre] + dronMadre[puntoMedioMadre:]
        viajanteHijo2 = dronMadre[:puntoMedioMadre] + dronPadre[puntoMedioPadre:]
        
        # controlamos que los caminos no sean vacios
        if len(viajanteHijo1) == 0:
            viajanteHijo1 = dronPadre
        if len(viajanteHijo2) == 0:
            viajanteHijo2 = dronMadre

        # metemos los nuevos caminos en la lista de drones
        listaDronesHijo1.append(viajanteHijo1)
        listaDronesHijo2.append(viajanteHijo2)

    # devolvemos las dos nuevas soluciones (PUEDEN NO SER VALIDAS)
    return listaDronesHijo1, listaDronesHijo2


# Funcion principal que ejecuta el algoritmo genetico para el problema de los drones y sensores
def genetico(listaSensores, tamano_poblacion, porcentaje_mejor, probabilidad_mutante, maximo_generaciones_sin_mejora, drones, peso_distancia):
    
    # hacemos una copia de la lista de sensores 
    copiaListaSensores = copy.deepcopy(listaSensores)

    # creamos una lista de soluciones
    listaSoluciones = []

    # variable de control para la primera generacion
    primera_generacion = True

    # inicializamos el mejor fitness a menos infinito
    mejor_fitness = -math.inf

    # inicializamos el numero de generaciones sin mejora a 0
    generaciones_sin_mejora = 0

    # mientras no se alcance el maximo de generaciones sin mejora
    while generaciones_sin_mejora < maximo_generaciones_sin_mejora:
        
        # Si estamos en la primera generacion
        if primera_generacion == True:
                
            primera_generacion = False

            # realizamos tantas veces como tamano de poblacion
            for iteracion in range(tamano_poblacion):
                
                # rehacemos una copia de la lista de sensores 
                copiaListaSensores = copy.deepcopy(listaSensores)

                # aleatorizamos la lista de los sensores dejando el sensor de origen en la primera posicion
                copiaListaSensores = [copiaListaSensores[0]] + random.sample(copiaListaSensores[1:], len(copiaListaSensores)-1)

                # generamos una solución aleatoria válida
                listaDrones = generaSolucion(copiaListaSensores, drones)

                # obtenemos el fitness de la solucion
                f = fitness(listaDrones, peso_distancia)

                # creamos una tupla con la solucion y su fitness
                solucion = [listaDrones, f]

                # anadimos la solucion a la lista de soluciones
                listaSoluciones.append(solucion)

        # para el resto de generaciones
        else:

            # hacemos una copia de las mejores soluciones para inicializar la lista de soluciones
            listaSoluciones = copy.deepcopy(mejoresSoluciones)
            
            # mientras no llegemos al tamaño de la poblacion
            while len(listaSoluciones) < tamano_poblacion:

                # seleccionamos aleatoriamente 2 padres
                padre, madre = [tupla[0] for tupla in random.sample(mejoresSoluciones, 2)]

                # generamos 2 nuevos hijos a partir de esos padres
                nuevosHijos = combinarSoluciones(padre, madre)

                # corregimos las soluciones, siendo sensor origen del hijo 1 la misma del padre, y sensor origen del hijo 2 la misma de la madre
                for hijo in nuevosHijos:
                    
                    # rehacemos una copia de la lista de sensores 
                    copiaListaSensores = copy.deepcopy(listaSensores)

                    # aleatorizamos la lista de los sensores dejando el sensor de origen en la primera posicion
                    copiaListaSensores = [copiaListaSensores[0]] + random.sample(copiaListaSensores[1:], len(copiaListaSensores)-1)

                    # corregimos una solución
                    listaDrones = corrigeSolucion(hijo, copiaListaSensores, drones)
                    
                    # mutamos si la probabilidad lo indica
                    if random.randint(1, 100) <= probabilidad_mutante:
                        listaDrones = mutante(listaDrones, drones)

                    # obtenemos el fitness de la solucion
                    f = fitness(listaDrones, peso_distancia)

                    # creamos una tupla con la solucion y su fitness
                    solucion = [listaDrones, f]

                    # anadimos la solucion a la lista de soluciones
                    listaSoluciones.append(solucion)
        
        # ordenamos las soluciones en funcion de su fitness con una funcion anonima que recibe el segundo elemento de la tupla
        listaSolucionesOrdenadas = sorted(listaSoluciones, key=lambda x: x[1], reverse=True)

        # Escogemos las mejores soluciones basandonos en un porcentaje predefinido
        mejoresSoluciones = listaSolucionesOrdenadas[:((tamano_poblacion * porcentaje_mejor) // 100)]
        
        # Comprobar si se ha alcanzado la estabilidad del fitness
        if mejoresSoluciones[0][1] > mejor_fitness:

            # Actualizamos el mejor fitness
            mejor_fitness = mejoresSoluciones[0][1]

            # Reiniciamos el contador de generaciones sin mejora
            generaciones_sin_mejora = 0

        else:

            # Incrementamos el contador de generaciones sin mejora
            generaciones_sin_mejora = generaciones_sin_mejora + 1
            
    # Devolvemos la mejor solucion
    return mejoresSoluciones[0]


# Funcion que recibe una lista de drones y la devuelve intercambiando dos sensores aleatoriamente
def mutante(listaDrones, drones):
    
    # Creamos una copia de la lista de drones
    copiaListaDrones = copy.deepcopy(listaDrones)
    
    # Seleccionamos un dron aleatorio
    dron = random.choice(copiaListaDrones)
    
    # Si el dron tiene menos de 3 sensores, no se puede mutar
    if len(dron) < 3:
        return copiaListaDrones
    
    # Seleccionamos dos sensores aleatorios del dron (que no sean el sensor de origen)
    sensor1 = random.choice(dron[1:])
    sensor2 = random.choice(dron[1:])
    
    # Intercambiamos los sensores
    dron[dron.index(sensor1)] = sensor2
    dron[dron.index(sensor2)] = sensor1
    
    # Calculamos la nueva distancia total recorrida
    distancia = distanciaTotalDron(dron)
    
    # Si la distancia supera la capacidad del dron, deshacemos la mutacion
    if distancia > drones[copiaListaDrones.index(dron)].get('distance_capacity'):
        dron[dron.index(sensor1)] = sensor1
        dron[dron.index(sensor2)] = sensor2
    
    # Devolvemos la lista de drones mutada (o no, si no se cumplen las condiciones)
    return copiaListaDrones


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


# Funcion auxiliar que genera una lista de colores unicos para los caminos de los drones
def generarColoresUnicos(n):
    listaColores = []
    pasoHue = 1.0 / n
    for i in range(n):
        hue = i * pasoHue
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        rgbInt = tuple(int(x * 255) for x in rgb)
        hexColor = '#{:02x}{:02x}{:02x}'.format(*rgbInt)
        listaColores.append(hexColor)
    return listaColores


# Funcion auxiliar para generar un grafico que muestre los caminos de los drones
def dibujarCaminos(mejorSolucion, listaSensores, drones):
    
    nTotalSensores = 0
    nCaminos = 0
    listaColores = generarColoresUnicos(len(drones))
    
    for dron in mejorSolucion[0]:
        nTotalSensores += len(dron) - 1
        x = []
        y = []
        for sensor in dron:
            x.append(sensor[0][0])
            y.append(sensor[0][1])
        x.append(dron[0][0][0])
        y.append(dron[0][0][1])
        plt.plot(x,y,":o",color=listaColores[nCaminos])
        nCaminos += 1
        
    # Obtenemos la lista de sensores no visitados por ningun dron comparando sus coordenadas
    sensoresNoVisitados = []
    for sensor in listaSensores:
        visitado = False
        for dron in mejorSolucion[0]:
            for sensorDron in dron:
                if sensor[0] == sensorDron[0]:
                    visitado = True
                    break
        if not visitado:
            sensoresNoVisitados.append(sensor)
    
    # Imprimimos los sensores no visitados en gris
    x = []
    y = []
    for sensor in sensoresNoVisitados:
        x.append(sensor[0][0])
        y.append(sensor[0][1])
    plt.scatter(x, y, color='gray')
    
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
    plt.title('Gráfico de Caminos')
    plt.text(mejorSolucion[0][0][0][0][0],mejorSolucion[0][0][0][0][1], " sensor origen")
    plt.show()


# Funcion auxiliar que escribe los resultados obtenidos por el algoritmo genetico en un fichero de log y por pantalla
def escribirResultados(mejorSolucion, tamano_poblacion, porcentaje_mejor, probabilidad_mutante, maximo_generaciones_sin_mejora, tiempo_total, drones, peso_distancia, listaSensores):
    
    copiaListaSensores = copy.deepcopy(listaSensores)
    
    # Establecemos a 0 la prioridad y la bateria del sensor de origen
    # Se hace para que al imprimir el escenario se vea que el sensor de origen tiene prioridad y bateria 0
    copiaListaSensores[0] = (copiaListaSensores[0][0], 0, 0)
    
    # Calculamos la distancia total, la bateria recargada y la prioridad acumulada por los drones
    distanciaTotal = 0
    bateriaTotal = 0
    prioridadTotal = 0
    resultadosDrones = []
    for i, dron in enumerate(mejorSolucion[0]):
        # Calculamos la distancia, prioridad y bateria total
        distanciaDron = distanciaTotalDron(dron)
        distanciaTotal += distanciaDron
        prioridadDron = prioridadTotalDron(dron)
        prioridadTotal += prioridadDron
        bateriaDron = bateriaTotalDron(dron)
        bateriaTotal += bateriaDron
        
        # Generamos el resultado del dron
        resultadoDron = f"\nDron {i+1} (C = {drones[i]['distance_capacity']}, B = {drones[i]['battery_capacity']}):"
        
        if len(dron) == 1:
            resultadoDron += f"\n- No hace ningun viaje"
        else:
            # recorremos los sensores del camino hasta el penultimo
            for j, sensor in enumerate(dron[:-1]):
                # Buscamos en la lista de sensores el index de los sensores con las mismas coordenadas que los sensores del camino
                # solo miramos las coordenadas, ya que la prioridad y la bateria de los sensores pueden diferir
                origen = copiaListaSensores.index([s for s in copiaListaSensores if s[0] == sensor[0]][0])
                destino = copiaListaSensores.index([s for s in copiaListaSensores if s[0] == dron[j+1][0]][0])
                resultadoDron += f"\n- Viaja de {origen + 1} a {destino + 1} (D += {distanciaEuclidea(sensor[0],dron[j+1][0])}, F += {int(dron[j+1][2])}, P += {int(dron[j+1][1])})"
            # Incluimos el regreso al sensor de origen
            origen = copiaListaSensores.index([s for s in copiaListaSensores if s[0] == dron[-1][0]][0])
            destino = copiaListaSensores.index([s for s in copiaListaSensores if s[0] == dron[0][0]][0])
            resultadoDron += f"\n- Viaja de {origen + 1} a {destino + 1} (D += {distanciaEuclidea(dron[-1][0],dron[0][0])})"
            resultadoDron += f"\n- Total del dron (D = {distanciaDron}, F = {int(bateriaDron)}, P = {int(prioridadDron)})"
        
        resultadosDrones.append(resultadoDron)
    
    # Calculamos la distancia maxima y bateria maxima recargable por los drones
    distanciaMaxima = sum(dron['distance_capacity'] for dron in drones)
    bateriaMaxima = sum(dron['battery_capacity'] for dron in drones)
    
    # Calculamos la prioridad maxima acumulable por los drones (sin contar el sensor de origen)  
    prioridadMaxima = sum(sensor[1] for sensor in copiaListaSensores[1:])
    
    # Calculamos los porcentajes de distancia, bateria y prioridad
    porcentajeDistancia = (distanciaTotal / distanciaMaxima) * 100
    porcentajeBateria = (bateriaTotal / bateriaMaxima) * 100
    porcentajePrioridad = (prioridadTotal / prioridadMaxima) * 100
    
    # Escribimos en el fichero de log los resultados obtenidos por el algoritmo genetico y cerramos el fichero
    f = open("Genetico/log_drones.txt", "a")
    string = f"{time.strftime('%d/%m/%Y, %H:%M:%S')}"
    string += "\n\n## RESULTADO ##" 
    string += f"\n\nFitness = {mejorSolucion[1]}"
    string += f"\nTiempo = {tiempo_total}"
    string += "\n" + "\n".join(resultadosDrones)
    string += f"\n\nDistancia (D) = {distanciaTotal} / {distanciaMaxima} ( {porcentajeDistancia}% )"
    string += f"\nBateria   (F) = {int(bateriaTotal)} / {int(bateriaMaxima)} ( {porcentajeBateria}% )"
    string += f"\nPrioridad (P) = {int(prioridadTotal)} / {int(prioridadMaxima)} ( {porcentajePrioridad}% )"
    string += "\n\n## PARAMETROS ##"
    string += f"\n\nPeso Distancia = {peso_distancia}"
    string += f"\nTamano Poblacion = {tamano_poblacion}"
    string += f"\nPorcentaje Mejor = {porcentaje_mejor}"
    string += f"\nProbabilidad Mutante = {probabilidad_mutante}"
    string += f"\nMaximo Generaciones sin Mejora = {maximo_generaciones_sin_mejora}"
    string += "\n\n## ESCENARIO ##"
    string += f"\n\n- Drones\nn = {len(drones)}\nC = [{', '.join(str(dron['distance_capacity']) for dron in drones)}]\nB = [{', '.join(str(dron['battery_capacity']) for dron in drones)}]"
    string += f"\n\n- Sensores\nm = {len(copiaListaSensores)}\ncoordSensor = [{', '.join(str(sensor[0]) for sensor in copiaListaSensores)}]\nF = [{', '.join(str(sensor[1]) for sensor in copiaListaSensores)}]\nP = [{', '.join(str(sensor[2]) for sensor in copiaListaSensores)}]"
    string += "\n\n\n\n\n"
    f.write(string)
    f.close()
    
    # Imprimimos lo mismo por pantalla
    print(string)


# Se ejecuta el programa
main()