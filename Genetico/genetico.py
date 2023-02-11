# Programa que resuelve el problema de los viajantes de ciudades mediante algoritmos genéticos

# importamos librerias
import re
import random
import math
import matplotlib.pyplot as plt
from random import randint

# Funcion main
def main():
    
    # Variables importantes configurables para el algoritmo genetico
    tamano_poblacion = 500
    porcentaje_mejor = 10
    maximo_generaciones = 100

    # definimos el numero de viajantes, en este caso 3 (MAXIMO = Numero de ciudades - 1, MINIMO = 1)
    num_viajantes = 3

    # Llamamos al algoritmo genetico
    mejorSolucion = genetico(tamano_poblacion, porcentaje_mejor, maximo_generaciones, num_viajantes)

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

    copiaListaViajantes = listaViajantes[:]
    copiaListaCiudades = listaCiudades[:]

    # Nos aseguramos de que la ciudad de origen es igual para todos los viajantes
    for viajante in copiaListaViajantes:
        viajante[0] = ciudadOrigen

    # Obtenemos una lista con las ciudades visitadas por los viajantes, sin añadir elementos repetidos
    ciudadesVisitadas = []
    for viajante in copiaListaViajantes:
        for ciudad in viajante:
            if ciudad not in ciudadesVisitadas:
                ciudadesVisitadas.append(ciudad)
            

    # Obtenemos una lista de las ciudades sin visitar
    ciudadesSinVisitar = [ciudad for ciudad in copiaListaCiudades if ciudad not in ciudadesVisitadas]

    # Repartir los elementos de la lista entre los viajantes
    for ciudad in ciudadesSinVisitar:

        # Verificamos si todos los viajantes tienen al menos una ciudad (a parte de la inicial)
        todos_tienen_elemento = True
        for viajante in copiaListaViajantes:
            if len(viajante) <= 1:
                todos_tienen_elemento = False
                viajante.append(ciudad)
                break

        # Si todos los viajantes tienen al menos una ciudad (a parte de la inicial), se asigna aleatoriamente
        if todos_tienen_elemento:
            # Elegir al azar a qué vector se añade el elemento
            viajante = random.choice(copiaListaViajantes)

            # Generamos un número aleatorio entre 0 y la longitud de la lista
            random_index = randint(1, len(viajante) - 1)

            # añadimos el elemento al viajante seleccionado en la posición aleatoria
            viajante.insert(random_index, ciudad)

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
        puntoMedioPadre = len(viajantePadre) // 2
        puntoMedioMadre = len(viajanteMadre) // 2

        # combinamos los caminos creando dos nuevos caminos
        viajanteHijo1 = viajantePadre[:puntoMedioPadre] + viajanteMadre[puntoMedioMadre:]
        viajanteHijo2 = viajanteMadre[:puntoMedioMadre] + viajantePadre[puntoMedioPadre:]

        # metemos los nuevos caminos en la lista de viajantes
        listaViajantesHijo1.append(viajanteHijo1)
        listaViajantesHijo2.append(viajanteHijo2)

    # devolvemos las dos nuevas soluciones (PUEDEN NO SER VALIDAS)
    return listaViajantesHijo1, listaViajantesHijo2

# Funcion principal que ejecuta el algoritmo genetico para el problema de los viajantes de ciudades
def genetico(tamano_poblacion, porcentaje_mejor, maximo_generaciones, num_viajantes):

    # Recuperamos las ciudades del .txt
    listaCiudades = recuperaCiudades()

    # hacemos una copia de la lista de ciudades 
    copiaListaCiudades = listaCiudades[:]

    # creamos una lista de soluciones
    listaSoluciones = []

    # realizamos tantas generaciones como maximo de generaciones
    for generacion in range(maximo_generaciones):
        
        # Si estamos en la primera generacion
        if generacion == 0:

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
            listaSoluciones = mejoresSoluciones[:]

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

    return mejoresSoluciones[0]

# Funcion auxiliar para generar un color aleatorio
def random_hex_color():
    red = format(random.randint(0, 255), '02x')
    green = format(random.randint(0, 255), '02x')
    blue = format(random.randint(0, 255), '02x')
    return '#' + red + green + blue

# Funcion auxiliar para generar un grafico que muestre los caminos de los viajantes
def imprimirCaminos(mejorSolucion):
    # Imprimimos la solución
    nCaminos = 0
    for viajante in mejorSolucion[0]:
        nCaminos += 1
        print("\n\nCamino del viajante [", nCaminos, "]: \n\n", viajante)
        x = []
        y = []
        for ciudad in viajante:
            x.append(ciudad[0])
            y.append(ciudad[1])
        x.append(viajante[0][0])
        y.append(viajante[0][1])
        plt.plot(x,y,":",color=random_hex_color())
        plt.xlabel('Eje X')
        plt.ylabel('Eje Y')
        plt.title('Gráfico de Caminos')
    plt.show()
    print("\nLa mínima distancia recorrida es: ", mejorSolucion[1], "\n\n\n")

# Se ejecuta el programa
main()