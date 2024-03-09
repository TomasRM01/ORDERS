# Programa que resuelve el problema de los drones de sensores mediante algoritmos genéticos

# importamos librerias
import copy
import re
import random
import math
import time
import matplotlib.pyplot as plt
from random import randint

# Funcion main
def main():
    
    # Variables importantes configurables para el algoritmo genetico
    tamano_poblacion = 1000
    porcentaje_mejor = 10
    probabilidad_mutante = 50
    maximo_generaciones_sin_mejora = 20
    
    # definimos el numero de drones, en este caso 3
    num_drones = 3
    
    # Definimos los valores minimos y maximos para las capacidades de los drones
    min_distance = 100
    max_distance = 150

    min_battery = 100
    max_battery = 250
    
    # Creamos una lista de drones con sus capacidades 
    #! Esto son valores aleatorios, si queremos COMPARAR escenarios, habria que cambiar esto
    drones = []
    for _ in range(num_drones):
        dron = {
            'distance_capacity': random.randint(min_distance, max_distance),  # distance capacity variable
            'battery_capacity': random.randint(min_battery, max_battery)  # battery capacity variable
        }
        drones.append(dron)
        
    # Recuperamos los sensores del .txt
    listaSensores = recuperaSensores()

    print("\n\n\n[Comenzando la ejecución del algoritmo genético]\n\n")
    
    # Arrancamos el cronometro
    inicio = time.time()
    
    # Llamamos al algoritmo genetico
    mejorSolucion = genetico(listaSensores, tamano_poblacion, porcentaje_mejor, probabilidad_mutante, maximo_generaciones_sin_mejora, num_drones, drones)

    # Paramos el cronometro y medimos el tiempo total
    fin = time.time()
    tiempo_total = fin - inicio
    
    print("\nEl algoritmo tardó [{}] segundos en ejecutarse.".format(tiempo_total))
    
    # Calculamos la distancia total, la bateria recargada y la prioridad acumulada por los drones
    distanciaTotal = 0
    bateriaTotal = 0
    prioridadTotal = 0
    for dron in mejorSolucion[0]:
        # Calculamos la distancia total recorrida por el dron
        distanciaDron = 0
        for i in range(len(dron) - 1):
            x1, y1 = dron[i][0]
            x2, y2 = dron[i + 1][0]
            distanciaDron += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        # Agregamos la distancia de retorno a la primera sensor
        x1, y1 = dron[-1][0]
        x2, y2 = dron[0][0]
        distanciaDron += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        distanciaTotal += distanciaDron
        # Calculamos la prioridad y bateria total recorrida por el dron
        prioridadDron = 0
        bateriaDron = 0
        for sensor in dron:
            prioridadDron += sensor[1]
            bateriaDron += sensor[2]
        prioridadTotal += prioridadDron
        bateriaTotal += bateriaDron
    
    # Escribimos en el fichero de log los resultados obtenidos por el algoritmo genetico y cerramos el fichero
    #TODO imprimir datos de los drones
    f = open("log_drones.txt", "a") 
    string = "############# RESULTADO ##############" 
    string += "\n\n---ENTRADAS---" 
    string += "\nNumero de drones: " + str(num_drones) 
    string += "\nTamano poblacion: " + str(tamano_poblacion) 
    string += "\nPorcentaje mejor: " + str(porcentaje_mejor) 
    string += "\nProbabilidad mutante: " + str(probabilidad_mutante) 
    string += "\nMaximo generaciones sin mejora: " + str(maximo_generaciones_sin_mejora) 
    string += "\n\n---SALIDAS---" 
    string += "\nTiempo: " + str(tiempo_total) 
    string += "\nFitness: " + str(mejorSolucion[1]) 
    string += "\n\n---CAMINOS---\n"
    for dron in mejorSolucion[0]:
        string = string + str(dron) + "\n"
    string += "\n---DISTANCIA, BATERIA Y PRIORIDAD---\n"
    string += "Distancia total recorrida por los drones: " + str(distanciaTotal) + "\n"
    string += "Bateria total recargada por los drones: " + str(bateriaTotal) + "\n"
    string += "Prioridad total acumulada por los drones: " + str(prioridadTotal) + "\n"
    string += "\n\n\n"
    f.write(string)
    f.close()

    # Imprimimos la mejor solucion con una grafica
    imprimirCaminos(mejorSolucion, listaSensores, drones)

# Funcion que lee el contenido de el fichero scenary_drones.txt y devuelve la lista de sensores con sus coordenadas
def recuperaSensores():
    
    # TODO cambiar para que cada sensor sea una tupla con sus coordenadas, prioridad y bateria, no tres listas separadas

    # lista de sensores
    sensores = []

    # abrimos el fichero en modo lectura
    with open("scenary_drones.txt", "r") as f:
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
def generaSolucion(listaSensores, num_drones, drones):
    
    # lista vacia de caminos para cada dron
    listaDrones = []
    
    for n in range(num_drones):
        listaDrones.append([])
    
    # copia de la lista de sensores
    copiaListaSensores = copy.deepcopy(listaSensores)
    
    # obtenemos sensor inicial y lo eliminamos de la lista de sensores
    sensorInicial = copiaListaSensores.pop(0)
    
    # actualizamos prioridad y bateria del sensor inicial a 0
    sensorInicial = (sensorInicial[0], 0, 0)
    
    #indice
    i = 0
    
    # para cada dron
    for dron in drones:
        
        # bateria y distancia restante del dron
        bateria = dron['battery_capacity']
        distancia = dron['distance_capacity']
        
        # incluimos el sensor inicial en el camino del dron
        listaDrones[i].append(sensorInicial)
        
        ultimoSensor = sensorInicial
        
        # mientras queden sensores por visitar, y el dron tenga bateria y distancia
        for sensor in copiaListaSensores:
            
            # calculamos la distancia euclidea entre el ultimo sensor visitado y el sensor seleccionado
            x1, y1 = ultimoSensor[0]
            x2, y2 = sensor[0]
            distanciaSensor = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            
            # sumamos la distancia entre el sensor seleccionado y el sensor inicial
            x1, y1 = sensor[0]
            x2, y2 = sensorInicial[0]
            distanciaSensorVuelta = distanciaSensor + math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            
            # si la bateria y la distancia restante del dron son suficientes para visitar el sensor seleccionado
            if bateria - sensor[2] > 0 and distancia - distanciaSensorVuelta > 0:
                
                bateria = bateria - sensor[2]
                distancia = distancia - distanciaSensor
                
                # incluimos el sensor seleccionado en el camino del dron
                listaDrones[i].append(sensor)
                
                copiaListaSensores.remove(sensor)
                
                # actualizamos el ultimo sensor visitado
                ultimoSensor = sensor
                
        i = i + 1
        
    # para comprobar que es correcto, haremos unos calculos de comprobacion (solo debug)
    # !DEBUG
    # id = 0
    # for dron in listaDrones:
    #     #calculamos la distancia total recorrida por el dron
    #     distancia = 0
    #     for i in range(len(dron) - 1):
    #         x1, y1 = dron[i][0]
    #         x2, y2 = dron[i + 1][0]
    #         distancia += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    #     #agregamos la distancia de retorno a la primera sensor
    #     x1, y1 = dron[-1][0]
    #     x2, y2 = dron[0][0]
    #     distancia += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    #     print("Distancia total recorrida por el dron: ", distancia, "Distancia de la que disponia: ", drones[id].get('distance_capacity'))
    #     # calculamos la bateria total recargada por el dron
    #     bateria = 0
    #     for sensor in dron:
    #         bateria += sensor[2]
    #     print("Bateria total recargada por el dron: ", bateria, "Bateria de la que disponia: ", drones[id].get('battery_capacity'))
    #     id = id + 1
    # !DEBUG

    # devolvemos una lista de sensores visitados para cada dron
    return listaDrones


# Funcion que corrige una solucion incorrecta, haciendola válida usando una lista de sensores general
# Devuelve una lista que contiene N listas con caminos validos
def corrigeSolucion(listaDrones, listaSensores, drones): 
    
    # Obtenemos el sensor de origen
    sensorOrigen = listaDrones[0][0]

    # Hacemos una copia de las listas para no modificarlas
    copiaListaDrones = copy.deepcopy(listaDrones)
    copialistaSensores = copy.deepcopy(listaSensores)
    
    # eliminamos el sensor con las mismas coordenadas que el sensor de origen de la lista de sensores
    for sensor in copialistaSensores:
        if sensor[0] == sensorOrigen[0]:
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
        for i in range(len(dron) - 1, -1, -1):  
            sensor = dron[i]
            # Si el sensor está repetido o tiene las mismas coordenadas que el sensor de origen
            if contadorSensores[sensor] > 1 or sensor[0] == sensorOrigen[0]: 
                # lo eliminamos de la lista
                dron.remove(sensor)
        
                
    # Una vez eliminados los sensores repetidos, comprobamos que no se superen las capacidades de los drones
    for dron in copiaListaDrones:
        # insertamos el sensor de origen al principio de la lista
        dron.insert(0, sensorOrigen)
        # calculamos la distancia total recorrida y la bateria recargada por el dron
        distancia = 0
        bateria = dron[0][2]
        for i in range(len(dron) - 1):
            x1, y1 = dron[i][0]
            x2, y2 = dron[i + 1][0]
            distancia += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            bateria += dron[i + 1][2]
        # agregamos la distancia de retorno al primer sensor
        x1, y1 = dron[-1][0]
        x2, y2 = dron[0][0]
        distancia += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        # si la distancia supera la capacidad del dron, eliminamos sensores aleatorios hasta que se cumplan las condiciones
        while distancia > drones[copiaListaDrones.index(dron)].get('distance_capacity') or bateria > drones[copiaListaDrones.index(dron)].get('battery_capacity'):
            # seleccionamos un sensor aleatorio para eliminar del camino del dron (menos el sensor de origen)
            sensor = random.choice(dron[1:])
            # eliminamos el sensor del camino del dron
            dron.remove(sensor)
            # recalculamos la distancia total recorrida y la bateria recargada por el dron
            distancia = 0
            bateria = 0
            for j in range(len(dron) - 1):
                x1, y1 = dron[j][0]
                x2, y2 = dron[j + 1][0]
                distancia += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                bateria += dron[j + 1][2]
            # agregamos la distancia de retorno al primer sensor
            x1, y1 = dron[-1][0]
            x2, y2 = dron[0][0]
            distancia += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
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
            
    # Comprobar que no se superen las capacidades de los drones para debug
    # !DEBUG
    # id = 0
    # numSensoresVisitados = 1
    # for dron in copiaListaDrones:
        
    #     # sumamos el numero de sensores visitados
    #     numSensoresVisitados += len(dron) - 1
        
    #     #calculamos la distancia total recorrida por el dron
    #     distancia = 0
    #     for i in range(len(dron) - 1):
    #         x1, y1 = dron[i][0]
    #         x2, y2 = dron[i + 1][0]
    #         distancia += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    #     #agregamos la distancia de retorno a la primera sensor
    #     x1, y1 = dron[-1][0]
    #     x2, y2 = dron[0][0]
    #     distancia += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    #     print("Distancia total recorrida por el dron: ", distancia, "Distancia de la que disponia: ", drones[id].get('distance_capacity'))
    #     # calculamos la bateria total recargada por el dron
    #     bateria = 0
    #     for sensor in dron:
    #         bateria += sensor[2]
    #     print("Bateria total recargada por el dron: ", bateria, "Bateria de la que disponia: ", drones[id].get('battery_capacity'))
        
    #     # si se ha superado la capacidad del dron o la distancia
    #     if distancia > drones[id].get('distance_capacity') or bateria > drones[id].get('battery_capacity'):
    #         print("ERROR: Se ha superado la capacidad del dron o la distancia") # ! ESTO HAY QUE ARREGLARLO
        
    #     id = id + 1
    # print("Numero de sensores visitados: ", numSensoresVisitados)
    # print("Numero de sensores no visitados: ", len(sensoresNoVisitados))
    # !DEBUG
    
    # por cada sensor no visitado, intentamos insertarlo en un dron aleatorio
    for i in range(len(sensoresNoVisitados) - 1, -1, -1):
        sensor = sensoresNoVisitados[i]
        # seleccionamos un dron aleatorio
        dron = random.choice(copiaListaDrones)
        # insertamos el sensor en una posición aleatoria del dron
        dron.insert(randint(1, len(dron)), sensor)
        # calculamos la distancia total recorrida y la bateria recargada por el dron
        distancia = 0
        bateria = 0
        for j in range(len(dron) - 1):
            x1, y1 = dron[j][0]
            x2, y2 = dron[j + 1][0]
            distancia += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            bateria += dron[j + 1][2]
        # agregamos la distancia de retorno al primer sensor
        x1, y1 = dron[-1][0]
        x2, y2 = dron[0][0]
        distancia += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        # si la distancia supera la capacidad del dron, eliminamos el sensor
        if distancia > drones[copiaListaDrones.index(dron)].get('distance_capacity') or bateria > drones[copiaListaDrones.index(dron)].get('battery_capacity'):
            dron.remove(sensor)
        else:
            # si el sensor se ha insertado correctamente, lo eliminamos de la lista de sensores no visitados
            sensoresNoVisitados.remove(sensor)

    # Comprobar que no se superen las capacidades de los drones para debug
    # !DEBUG
    # id = 0
    # numSensoresVisitados = 1
    # for dron in copiaListaDrones:
        
    #     # sumamos el numero de sensores visitados
    #     numSensoresVisitados += len(dron) - 1
        
    #     #calculamos la distancia total recorrida por el dron
    #     distancia = 0
    #     for i in range(len(dron) - 1):
    #         x1, y1 = dron[i][0]
    #         x2, y2 = dron[i + 1][0]
    #         distancia += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    #     #agregamos la distancia de retorno a la primera sensor
    #     x1, y1 = dron[-1][0]
    #     x2, y2 = dron[0][0]
    #     distancia += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    #     print("Distancia total recorrida por el dron: ", distancia, "Distancia de la que disponia: ", drones[id].get('distance_capacity'))
    #     # calculamos la bateria total recargada por el dron
    #     bateria = 0
    #     for sensor in dron:
    #         bateria += sensor[2]
    #     print("Bateria total recargada por el dron: ", bateria, "Bateria de la que disponia: ", drones[id].get('battery_capacity'))
        
    #     # si se ha superado la capacidad del dron o la distancia
    #     if distancia > drones[id].get('distance_capacity') or bateria > drones[id].get('battery_capacity'):
    #         print("ERROR: Se ha superado la capacidad del dron o la distancia") # ! ESTO HAY QUE ARREGLARLO
        
    #     id = id + 1
    # print("Numero de sensores visitados: ", numSensoresVisitados)
    # print("Numero de sensores no visitados: ", len(sensoresNoVisitados))
    # !DEBUG
    
    # Devolver los vectores como una tupla
    return copiaListaDrones

# Funcion que recibe una posible solución, calcula las distancias euclídeas de todos los caminos, y devuelve el fitness de la solución
def fitness(listaDrones):
    
    #TODO ahora el fitness deberia incluir no solo la distancia, sino tambien la prioridad total

    # definimos un peso para la distancia
    pesoDistancia = 0.001

    # definimos una variable para el fitness
    f = 0.0

    # calculamos la distancia total recorrida por los drones
    distancia = 0
    for dron in listaDrones:
        for i in range(len(dron) - 1):
            x1, y1 = dron[i][0]
            x2, y2 = dron[i + 1][0]
            distancia += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        # agregamos la distancia de retorno al primer sensor
        x1, y1 = dron[-1][0]
        x2, y2 = dron[0][0]
        distancia += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
    # calculamos la prioridad total recorrida por los drones
    prioridad = 0
    for dron in listaDrones:
        for sensor in dron:
            prioridad += sensor[1]
            
    # la funcion de fitness es la prioridad menos la distancia por el peso de la distancia
    f = ((pesoDistancia * distancia) - prioridad)

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

        # prints de control            
        # print("puntoMedioPadre: ", puntoMedioPadre, "len(viajantePadre): ", len(viajantePadre))
        # print("puntoMedioMadre: ", puntoMedioMadre, "len(viajanteMadre): ", len(viajanteMadre))
        
        # combinamos los caminos creando dos nuevos caminos
        viajanteHijo1 = dronPadre[:puntoMedioPadre] + dronMadre[puntoMedioMadre:]
        viajanteHijo2 = dronMadre[:puntoMedioMadre] + dronPadre[puntoMedioPadre:]
        
        # controlamos que los caminos no sean vacios
        if len(viajanteHijo1) == 0:
            # print de control
            # print("ERROR: viajanteHijo1 vacio")
            viajanteHijo1 = dronPadre
            
        if len(viajanteHijo2) == 0:
            # print de control
            # print("ERROR: viajanteHijo2 vacio")
            viajanteHijo2 = dronMadre

        # metemos los nuevos caminos en la lista de drones
        listaDronesHijo1.append(viajanteHijo1)
        listaDronesHijo2.append(viajanteHijo2)

    # devolvemos las dos nuevas soluciones (PUEDEN NO SER VALIDAS)
    return listaDronesHijo1, listaDronesHijo2

# Funcion principal que ejecuta el algoritmo genetico para el problema de los drones y sensores
def genetico(listaSensores, tamano_poblacion, porcentaje_mejor, probabilidad_mutante, maximo_generaciones_sin_mejora, num_drones, drones):
    
    # hacemos una copia de la lista de sensores 
    copiaListaSensores = copy.deepcopy(listaSensores)

    # creamos una lista de soluciones
    listaSoluciones = []

    # variable de control para la primera generacion
    primera_generacion = True

    # inicializamos el mejor fitness a infinito
    mejor_fitness = math.inf

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

                # aleatorizamos la lista de los sensores
                random.shuffle(copiaListaSensores)

                # generamos una solución aleatoria válida
                listaDrones = generaSolucion(copiaListaSensores, num_drones, drones)

                # obtenemos el fitness de la solucion
                distancia = fitness(listaDrones)

                # creamos una tupla con la solucion y su fitness
                solucion = [listaDrones, distancia]

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

                    # aleatorizamos la lista de los sensores
                    random.shuffle(copiaListaSensores)

                    # corregimos una solución
                    listaDrones = corrigeSolucion(hijo, copiaListaSensores, drones)
                    
                    # # mutamos si la probabilidad lo indica
                    # if random.randint(1, 100) <= probabilidad_mutante:
                    #     listaDrones = mutante(listaDrones)

                    # obtenemos el fitness de la solucion
                    distancia = fitness(listaDrones)

                    # creamos una tupla con la solucion y su fitness
                    solucion = [listaDrones, distancia]

                    # anadimos la solucion a la lista de soluciones
                    listaSoluciones.append(solucion)
        
        # ordenamos las soluciones en funcion de su fitness con una funcion anonima que recibe el segundo elemento de la tupla
        listaSolucionesOrdenadas = sorted(listaSoluciones, key=lambda x: x[1])

        # Escogemos las mejores soluciones basandonos en un porcentaje predefinido
        mejoresSoluciones = listaSolucionesOrdenadas[:((tamano_poblacion * porcentaje_mejor) // 100)]
        
        # Comprobar si se ha alcanzado la estabilidad del fitness
        if mejoresSoluciones[0][1] < mejor_fitness:
            
            # Print de control para ver si el algoritmo encuentra mejores soluciones que la funcion generaSolucion()
            if  mejor_fitness != math.inf:
                print("HAY MEJORA: ", mejoresSoluciones[0][1])

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
def mutante(listaDrones):
    
    # Creamos una copia de la lista de drones
    
    copiaListaDrones = copy.deepcopy(listaDrones)
    
    # Seleccionamos dos drones aleatoriamente, pudiendo ser el mismo viajante
    
    viajante_a = random.randint(0, len(copiaListaDrones) - 1)
    viajante_b = random.randint(0, len(copiaListaDrones) - 1)
    
    # Si los drones seleccionados tienen mas de una sensor (sensor origen), seleccionamos dos sensores aleatoriamente de los drones seleccionados
    
    #TODO comprobar tambien que al intercambiar dichos sensores, no se superen las capacidades de los drones
    #TODO en su defecto, llamamos directamente a la funcion corrigeSolucion para que se encargue de ello
    
    if (len(copiaListaDrones[viajante_a]) > 1 and len(copiaListaDrones[viajante_b]) > 1):
        
        # Seleccionamos dos sensores aleatoriamente de los drones seleccionados, excluyendo la primera sensor de cada viajante (sensor origen)
        
        sensor_a = random.randint(1, len(copiaListaDrones[viajante_a]) - 1)
        sensor_b = random.randint(1, len(copiaListaDrones[viajante_b]) - 1)
    
        # Intercambiamos las sensores seleccionadas
        
        aux = copiaListaDrones[viajante_a][sensor_a]
        copiaListaDrones[viajante_a][sensor_a] = copiaListaDrones[viajante_b][sensor_b]
        copiaListaDrones[viajante_b][sensor_b] = aux
    
    # Devolvemos la lista de drones mutada (o no, si no se cumplen las condiciones)

    return copiaListaDrones

# Funcion auxiliar para generar un color aleatorio
def random_hex_color():
    red = format(random.randint(0, 255), '02x')
    green = format(random.randint(0, 255), '02x')
    blue = format(random.randint(0, 255), '02x')
    return '#' + red + green + blue

# Funcion auxiliar para generar un grafico que muestre los caminos de los drones
def imprimirCaminos(mejorSolucion, listaSensores, drones):
    
    # Imprimimos la solución
    nTotalSensores = 0
    nCaminos = 0
    
    prioridadTotal = 0
    bateriaTotal = 0
    distanciaTotal = 0
    
    for dron in mejorSolucion[0]:
        
        # Calculamos la distancia total recorrida por el dron
        distanciaDron = 0
        for i in range(len(dron) - 1):
            x1, y1 = dron[i][0]
            x2, y2 = dron[i + 1][0]
            distanciaDron += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        # Agregamos la distancia de retorno a la primera sensor
        x1, y1 = dron[-1][0]
        x2, y2 = dron[0][0]
        distanciaDron += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        # Calculamos la prioridad total recorrida por el dron
        prioridadDron = 0
        for sensor in dron:
            prioridadDron += sensor[1]
            
        # Calculamos la bateria total recargada por el dron
        bateriaDron = 0
        for sensor in dron:
            bateriaDron += sensor[2]
            
        
        distanciaTotal += distanciaDron
        bateriaTotal += bateriaDron
        prioridadTotal += prioridadDron
        
        nCaminos += 1
        print("\n\nCamino del dron [", nCaminos, "]: \n\n", dron)
        print("\nNúmero de sensores recorridos: ", len(dron) - 1, "\n\n")
        print("Distancia recorrida por el dron: ", distanciaDron, " / ", drones[nCaminos - 1].get('distance_capacity'))
        print("Bateria recargada por el dron: ", bateriaDron, " / ", drones[nCaminos - 1].get('battery_capacity'))
        print("Prioridad obtenida por el dron: ", prioridadDron)
        nTotalSensores += len(dron) - 1
        x = []
        y = []
        for sensor in dron:
            x.append(sensor[0][0])
            y.append(sensor[0][1])
        x.append(dron[0][0][0])
        y.append(dron[0][0][1])
        plt.plot(x,y,":o",color=random_hex_color())
        
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
    print("\n\nNúmero total de sensores recorridos: ", nTotalSensores + 1)
    print("Distancia total recorrida por todos los drones: ", distanciaTotal)
    print("Bateria total recargada por todos los drones: ", bateriaTotal)
    print("Prioridad total acumulada por todos los drones: ", prioridadTotal)
    plt.text(mejorSolucion[0][0][0][0][0],mejorSolucion[0][0][0][0][1], " sensor origen")
    print("\nFitness: ", mejorSolucion[1], "\n\n\n")
    plt.show()

# Se ejecuta el programa
main()