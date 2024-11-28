# Programa que resuelve el problema de los drones de sensores mediante algoritmos genéticos

# importamos librerias
import copy
import random
import math
import time
from aux_genetico_drones import distanciaTotalDron, prioridadTotalDron, bateriaTotalDron, distanciaEuclidea


# Funcion startGenetico que ejecuta el algoritmo genetico para el problema de los drones y sensores
def startGenetico(peso_distancia, tamano_poblacion, porcentaje_mejor, probabilidad_cruce, probabilidad_mutante, maximo_generaciones_sin_mejora, drones, listaSensores):
    
    # Arrancamos el cronometro
    inicio = time.time()
    
    # Llamamos al algoritmo genetico
    mejorSolucion = genetico(listaSensores, tamano_poblacion, porcentaje_mejor, probabilidad_cruce, probabilidad_mutante, maximo_generaciones_sin_mejora, drones, peso_distancia)

    # Paramos el cronometro y medimos el tiempo total
    fin = time.time()
    tiempo_total = fin - inicio
    
    # Devolvemos el fitness de la mejor solución
    return (mejorSolucion[0], mejorSolucion[1], tiempo_total)


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
        dron.insert(random.randint(1, len(dron)), sensor)
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
def genetico(listaSensores, tamano_poblacion, porcentaje_mejor, probabilidad_cruce, probabilidad_mutante, maximo_generaciones_sin_mejora, drones, peso_distancia):
    
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

                # hacemos el cruce solo si la probabilidad lo indica
                if random.random() < probabilidad_cruce:
                    # generamos 2 nuevos hijos a partir de esos padres
                    nuevosHijos = combinarSoluciones(padre, madre)
                else:
                    # si no se cumple la probabilidad de cruce, los hijos serán copias de los padres
                    nuevosHijos = [copy.deepcopy(padre), copy.deepcopy(madre)]

                # corregimos las soluciones, siendo sensor origen del hijo 1 la misma del padre, y sensor origen del hijo 2 la misma de la madre
                for hijo in nuevosHijos:
                    
                    # rehacemos una copia de la lista de sensores 
                    copiaListaSensores = copy.deepcopy(listaSensores)

                    # aleatorizamos la lista de los sensores dejando el sensor de origen en la primera posicion
                    copiaListaSensores = [copiaListaSensores[0]] + random.sample(copiaListaSensores[1:], len(copiaListaSensores)-1)

                    # corregimos una solución
                    listaDrones = corrigeSolucion(hijo, copiaListaSensores, drones)
                    
                    # mutamos si la probabilidad lo indica
                    if random.random() < probabilidad_mutante:
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
