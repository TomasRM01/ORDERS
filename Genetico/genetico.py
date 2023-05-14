# Programa que resuelve el problema de los viajantes de ciudades mediante algoritmos genéticos

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
    maximo_generaciones_sin_mejora = 100
    
    # definimos el numero de viajantes, en este caso 3
    num_viajantes = 3

    print("\n\n\n[Comenzando la ejecución del algoritmo genético]\n\n")
    
    # Arrancamos el cronometro
    inicio = time.time()
    
    # Llamamos al algoritmo genetico
    mejorSolucion = genetico(tamano_poblacion, porcentaje_mejor, probabilidad_mutante, maximo_generaciones_sin_mejora, num_viajantes)

    # Paramos el cronometro y medimos el tiempo total
    fin = time.time()
    tiempo_total = fin - inicio
    
    print("\nEl algoritmo tardó [{}] segundos en ejecutarse.".format(tiempo_total))
    
    # Escribimos en el fichero de log los resultados obtenidos por el algoritmo genetico y cerramos el fichero
    f = open("log.txt", "a") 
    string = "############# RESULTADO ##############" 
    string += "\n\n---ENTRADAS---" 
    string += "\nNumero de viajantes: " + str(num_viajantes) 
    string += "\nTamano poblacion: " + str(tamano_poblacion) 
    string += "\nPorcentaje mejor: " + str(porcentaje_mejor) 
    string += "\nProbabilidad mutante: " + str(probabilidad_mutante) 
    string += "\nMaximo generaciones sin mejora: " + str(maximo_generaciones_sin_mejora) 
    string += "\n\n---SALIDAS---" 
    string += "\nTiempo: " + str(tiempo_total) 
    string += "\nDistancia: " + str(mejorSolucion[1]) 
    string += "\n\n---CAMINOS---\n"
    for viajante in mejorSolucion[0]:
        string = string + str(viajante) + "\n"
    string += "\n\n\n"
    f.write(string)
    f.close()

    # Imprimimos la mejor solucion con una grafica
    imprimirCaminos(mejorSolucion)

# Funcion que lee el contenido de el fichero scenary.txt y devuelve la lista de ciudades con sus coordenadas
def recuperaCiudades():

    # definimos lista de posiciones
    posiciones = []

    # abrimos el fichero en modo lectura
    f = open("scenary.txt", "r")

    # pasamos el contenido a un string
    s = f.read()

    # cerramos el fichero
    f.close()

    # desechamos todo lo que no son numeros y lo convertimos en una lista de elementos
    s = [float(s) for s in re.findall(r'\d+\.?\d*', s)]

    # para cada elemento de la lista, si su index es par lo guardamos en 'x' y si es impar,
    # lo guardamos en 'y' y agregamos la tupla a la lista de posiciones
    contador = 0
    for element in s:
        if contador % 2:
            y = element
            posiciones.append((x, y))
        else:
            x = element
        contador = contador + 1

    return posiciones

# Funcion que genera una solucion aleatoria valida a partir de una lista de ciudades (con orden previamente aleatorizado)
# para N viajantes, devuelve una lista que contiene N listas con sus respectivos caminos
def generaSolucion(listaCiudades, num_viajantes):

    # Crear la lista de vectores vacíos
    lista_viajantes = []
    for i in range(num_viajantes):
        lista_viajantes.append([])

    # Repartir los elementos de la lista entre los viajantes
    for ciudad in listaCiudades[1:]:

        # Verificamos si todos los viajantes tienen al menos una ciudad
        todos_tienen_elemento = True
        for viajante in lista_viajantes:
            if len(viajante) == 0:
                todos_tienen_elemento = False
                viajante.append(ciudad)
                break

        # Si todos los viajantes tienen al menos una ciudad, se asigna aleatoriamente
        if todos_tienen_elemento:
            # Elegir al azar a qué vector se añade el elemento
            viajante = random.choice(lista_viajantes)

            # añadimos el elemento al viajante seleccionado
            viajante.append(ciudad)

    # Añadir el primer elemento a los vectores
    for v in lista_viajantes:
        v.insert(0, listaCiudades[0])

    # Devolver los vectores como una tupla
    return lista_viajantes

# Funcion que corrige una solucion incorrecta, haciendola válida usando una lista de ciudades (con orden previamente aleatorizado)
# y usando la primera como ciudad inicial. Devuelve una lista que contiene N listas con caminos validos
def corrigeSolucion(listaViajantes, listaCiudades, ciudadOrigen):

    # Hacemos una copia de las listas para no modificarlas
    copiaListaViajantes = copy.deepcopy(listaViajantes)
    copiaListaCiudades = copy.deepcopy(listaCiudades)

    # Obtenemos una lista con las ciudades visitadas por los viajantes (sin repeticiones)
    ciudadesVisitadas = []
    ciudadesRepetidas = []
    for viajante in copiaListaViajantes:
        for ciudad in viajante:
            if ciudad not in ciudadesVisitadas:
                ciudadesVisitadas.append(ciudad)
            else:
                if ciudad not in ciudadesRepetidas:
                    ciudadesRepetidas.append(ciudad)

    for viajante in copiaListaViajantes:
        for ciudad in viajante[:]:
            if ciudad in ciudadesRepetidas:
                viajante.remove(ciudad)

    # Obtenemos una lista de las ciudades sin visitar
    ciudadesSinVisitar = [ciudad for ciudad in copiaListaCiudades if ciudad not in ciudadesVisitadas]

    ciudadesSinVisitar += ciudadesRepetidas

    if ciudadOrigen in ciudadesSinVisitar:
        ciudadesSinVisitar.remove(ciudadOrigen)

    # Repartir los elementos de la lista entre los viajantes
    for ciudad in ciudadesSinVisitar:

        # ordenamos la lista de viajantes por longitud
        copiaListaViajantes = sorted(copiaListaViajantes, key=lambda x: len(x))

        # Elegimos el viajante con menos elementos
        viajante = copiaListaViajantes[0]

        # Generamos un número aleatorio entre 0 y la longitud de la lista
        if len(viajante) == 0:
            random_index = 0
        else:
            random_index = randint(0, len(viajante) - 1)

        # añadimos el elemento al viajante seleccionado en la posición aleatoria
        viajante.insert(random_index, ciudad)
    
    # Nos aseguramos de que la ciudad de origen es igual para todos los viajantes
    for viajante in copiaListaViajantes:
        if len(viajante) == 0 or viajante[0] != ciudadOrigen:
            # insertamos ciudadOrigen en la primera posicion del viajante
            viajante.insert(0, ciudadOrigen)

    # Devolver los vectores como una tupla
    return copiaListaViajantes

# Funcion que recibe una posible solución, calcula las distancias euclídeas de todos los caminos, y devuelve el fitness de la solución
def fitness(listaViajantes):

    # definimos una variable para el fitness
    f = 0.0

    # para cada viajante de la lista de viajantes
    for viajante in listaViajantes:
        # para cada ciudad del camino
        for i in range(len(viajante) - 1):

            # obtenemos las coordenadas de las dos ciudades contiguas en el camino
            x1, y1 = viajante[i]
            x2, y2 = viajante[i + 1]

            # distancia euclidea
            distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

            # la sumamos al total
            f += distancia

        # agregamos la distancia de retorno a la primera ciudad
        x1, y1 = viajante[-1]
        x2, y2 = viajante[0]

        # distancia euclidea
        distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        # la sumamos al total
        f += distancia

    # devolvemos el fitness de la solución
    return f

# Funcion que recibe dos soluciones correctas y las combina, creando dos nuevas soluciones. Estas soluciones NO son correctas, es decir, hay que 
# corregirlas con la función corrigeSolucion
def combinarSoluciones(listaViajantesPadre, listaViajantesMadre):

    # Creamos dos listas vacias para devolver las posibles soluciones
    listaViajantesHijo1 = []
    listaViajantesHijo2 = []
    
    # para cada viajante de las dos soluciones
    for viajantePadre, viajanteMadre in zip(listaViajantesPadre, listaViajantesMadre):

        # calculamos los puntos medios de los vectores
        if len(viajantePadre) == 1:
            puntoMedioPadre = 0
        else:
            puntoMedioPadre = len(viajantePadre) // random.randint(1, len(viajantePadre) - 1)

        if len(viajanteMadre) == 1:
            puntoMedioMadre = 0
        else:
            puntoMedioMadre = len(viajanteMadre) // random.randint(1, len(viajanteMadre) - 1)

        # prints de control            
        # print("puntoMedioPadre: ", puntoMedioPadre, "len(viajantePadre): ", len(viajantePadre))
        # print("puntoMedioMadre: ", puntoMedioMadre, "len(viajanteMadre): ", len(viajanteMadre))
        
        # combinamos los caminos creando dos nuevos caminos
        viajanteHijo1 = viajantePadre[:puntoMedioPadre] + viajanteMadre[puntoMedioMadre:]
        viajanteHijo2 = viajanteMadre[:puntoMedioMadre] + viajantePadre[puntoMedioPadre:]
        
        # controlamos que los caminos no sean vacios
        if len(viajanteHijo1) == 0:
            # print de control
            # print("ERROR: viajanteHijo1 vacio")
            viajanteHijo1 = viajantePadre
            
        if len(viajanteHijo2) == 0:
            # print de control
            # print("ERROR: viajanteHijo2 vacio")
            viajanteHijo2 = viajanteMadre

        # metemos los nuevos caminos en la lista de viajantes
        listaViajantesHijo1.append(viajanteHijo1)
        listaViajantesHijo2.append(viajanteHijo2)

    # devolvemos las dos nuevas soluciones (PUEDEN NO SER VALIDAS)
    return listaViajantesHijo1, listaViajantesHijo2

# Funcion principal que ejecuta el algoritmo genetico para el problema de los viajantes de ciudades
def genetico(tamano_poblacion, porcentaje_mejor, probabilidad_mutante, maximo_generaciones_sin_mejora, num_viajantes):

    # Recuperamos las ciudades del .txt
    listaCiudades = recuperaCiudades()

    # hacemos una copia de la lista de ciudades 
    copiaListaCiudades = copy.deepcopy(listaCiudades)

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

                # aleatorizamos la lista de las ciudades
                random.shuffle(copiaListaCiudades)

                # generamos una solución aleatoria válida
                listaViajantes = generaSolucion(copiaListaCiudades, num_viajantes)

                # obtenemos el fitness de la solucion
                distancia = fitness(listaViajantes)

                # creamos una tupla con la solucion y su fitness
                solucion = [listaViajantes, distancia]

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

                # corregimos las soluciones, siendo ciudad origen del hijo 1 la misma del padre, y ciudad origen del hijo 2 la misma de la madre
                for hijo in nuevosHijos:

                    # corregimos una solución
                    listaViajantes = corrigeSolucion(hijo, listaCiudades, hijo[0][0])
                    
                    # mutamos si la probabilidad lo indica
                    if random.randint(1, 100) <= probabilidad_mutante:
                        listaViajantes = mutante(listaViajantes)

                    # obtenemos el fitness de la solucion
                    distancia = fitness(listaViajantes)

                    # creamos una tupla con la solucion y su fitness
                    solucion = [listaViajantes, distancia]

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

# Funcion que recibe una lista de viajantes y la devuelve intercambiando dos ciudades aleatoriamente
def mutante(listaViajantes):
    
    # Creamos una copia de la lista de viajantes
    
    copiaListaViajantes = copy.deepcopy(listaViajantes)
    
    # Seleccionamos dos viajantes aleatoriamente, pudiendo ser el mismo viajante
    
    viajante_a = random.randint(0, len(copiaListaViajantes) - 1)
    viajante_b = random.randint(0, len(copiaListaViajantes) - 1)
    
    # Si los viajantes seleccionados tienen mas de una ciudad (ciudad origen), seleccionamos dos ciudades aleatoriamente de los viajantes seleccionados
    
    if (len(copiaListaViajantes[viajante_a]) > 1 and len(copiaListaViajantes[viajante_b]) > 1):
        
        # Seleccionamos dos ciudades aleatoriamente de los viajantes seleccionados, excluyendo la primera ciudad de cada viajante (ciudad origen)
        
        ciudad_a = random.randint(1, len(copiaListaViajantes[viajante_a]) - 1)
        ciudad_b = random.randint(1, len(copiaListaViajantes[viajante_b]) - 1)
    
        # Intercambiamos las ciudades seleccionadas
        
        aux = copiaListaViajantes[viajante_a][ciudad_a]
        copiaListaViajantes[viajante_a][ciudad_a] = copiaListaViajantes[viajante_b][ciudad_b]
        copiaListaViajantes[viajante_b][ciudad_b] = aux
    
    # Devolvemos la lista de viajantes mutada (o no, si no se cumplen las condiciones)

    return copiaListaViajantes

# Funcion auxiliar para generar un color aleatorio
def random_hex_color():
    red = format(random.randint(0, 255), '02x')
    green = format(random.randint(0, 255), '02x')
    blue = format(random.randint(0, 255), '02x')
    return '#' + red + green + blue

# Funcion auxiliar para generar un grafico que muestre los caminos de los viajantes
def imprimirCaminos(mejorSolucion):
    totalCiudades = 0
    # Imprimimos la solución
    nCaminos = 0
    for viajante in mejorSolucion[0]:
        nCaminos += 1
        print("\n\nCamino del viajante [", nCaminos, "]: \n\n", viajante)
        print("\nNúmero de ciudades recorridas: ", len(viajante) - 1, "\n\n")
        totalCiudades += len(viajante) - 1
        x = []
        y = []
        for ciudad in viajante:
            x.append(ciudad[0])
            y.append(ciudad[1])
        x.append(viajante[0][0])
        y.append(viajante[0][1])
        plt.plot(x,y,":o",color=random_hex_color())
        plt.xlabel('Eje X')
        plt.ylabel('Eje Y')
        plt.title('Gráfico de Caminos')
    print("\n\nNúmero total de ciudades recorridas: ", totalCiudades + 1)
    plt.text(mejorSolucion[0][0][0][0],mejorSolucion[0][0][0][1], " Ciudad origen")
    print("\nLa mínima distancia recorrida es: ", mejorSolucion[1], "\n\n\n")
    plt.show()

# Se ejecuta el programa
main()