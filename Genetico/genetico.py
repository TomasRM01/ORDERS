# Programa que resuelve el problema de los viajantes de ciudades mediante algoritmos genéticos

# importamos librerias
import re
import random
from random import randint

# Funcion principal
def main():
    
    # Recuperamos las ciudades del .txt
    listaCiudades = recuperaCiudades()

    # hacemos una copia de la lista de ciudades 
    copiaListaCiudades = listaCiudades[:]

    # aleatorizamos la lista de las ciudades
    random.shuffle(copiaListaCiudades)

    # generamos una solución aleatoria válida
    listaViajantes = generaSolucion(copiaListaCiudades)

    # corregimos la solución (no hace nada, pues ya era válida)
    nuevaListaViajantes = corrigeSolucion(listaViajantes, copiaListaCiudades)

    # print de control: imprimimos los caminos
    for viajante in nuevaListaViajantes:
        print(viajante, "\n")

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
# para 3 viajantes, devuelve una lista que contiene tres listas con sus respectivos caminos
def generaSolucion(listaCiudades):

    # Extraer el primer elemento de la lista
    primera_ciudad = listaCiudades[0]

    # Crear los vectores vacíos
    viajante1 = []
    viajante2 = []
    viajante3 = []

    # Repartir los elementos de la lista entre los viajantes
    for ciudad in listaCiudades:
        if ciudad != primera_ciudad:

            # Elegir al azar a qué vector se añade el elemento
            viajante = random.choice([viajante1, viajante2, viajante3])

            # controlamos que ningun vector se quede sin al menos un elemento
            if len(viajante1) == 0:
                viajante = viajante1
            if len(viajante2) == 0:
                viajante = viajante2
            if len(viajante3) == 0:
                viajante = viajante3

            # añadimos el elemento al viajante seleccionado
            viajante.append(ciudad)

    # Añadir el primer elemento a los vectores
    viajante1.insert(0, primera_ciudad)
    viajante2.insert(0, primera_ciudad)
    viajante3.insert(0, primera_ciudad)

    # Devolver los vectores como una tupla
    return viajante1, viajante2, viajante3

# Funcion que corrige una solucion incorrecta, haciendola válida usando una lista de ciudades (con orden previamente aleatorizado)
# y usando la primera como ciudad inicial. Devuelve una lista que contiene tres listas con caminos validos
def corrigeSolucion(listaViajantes, listaCiudades):

    copiaListaViajantes = listaViajantes[:]
    copiaListaCiudades = listaCiudades[:]

    # extraemos las listas de ciudades de cada viajante
    viajante1 = copiaListaViajantes[0]
    viajante2 = copiaListaViajantes[1]
    viajante3 = copiaListaViajantes[2]

    # Nos aseguramos de que la ciudad de origen es igual para los tres viajantes
    ciudadOrigen = copiaListaCiudades[0]
    viajante1[0] = ciudadOrigen
    viajante2[0] = ciudadOrigen
    viajante3[0] = ciudadOrigen

    # objenemos una lista con las ciudades visitadas por los viajantes, eliminando elementos repetidos
    ciudadesVisitadas = set(viajante1 + viajante2 + viajante3)

    # print de control para ver si esta funcionando
    # print("ciudades visitadas:", len(ciudadesVisitadas))

    # Obtenemos una lista de las ciudades sin visitar
    ciudadesSinVisitar = []
    
    for ciudad in copiaListaCiudades:
        # Si la ciudad no ha sido visitada, la agregamos a la lista
        if ciudad not in ciudadesVisitadas:
            ciudadesSinVisitar.append(ciudad)

    # print de control para ver si esta funcionando
    # print("ciudades sin visitar:", len(ciudadesSinVisitar))

    # Repartir los elementos de la lista entre los viajantes
    for ciudad in ciudadesSinVisitar:
            # Elegir al azar a qué vector se añade el elemento
            viajante = random.choice([viajante1, viajante2, viajante3])

            # controlamos que ningun vector se quede sin al menos un elemento
            if len(viajante1) == 0:
                viajante = viajante1
            if len(viajante2) == 0:
                viajante = viajante2
            if len(viajante3) == 0:
                viajante = viajante3

            # Generamos un número aleatorio entre 0 y la longitud de la lista
            random_index = randint(1, len(viajante) - 1)

            # añadimos el elemento al viajante seleccionado en la posicion aleatoria
            viajante1.insert(random_index, ciudad)

    # print de control para ver si esta funcionando
    # comprobamos que la solución es válida
    # if (len(set(viajante1 + viajante2 + viajante3))) != len(copiaListaCiudades):
    #     print("error: no se recorren todas las ciudades")
    # else:
    #     print("se recorren todas las ciudades")

    # Devolver los vectores como una tupla
    return viajante1, viajante2, viajante3

# Se ejecuta el programa
main()