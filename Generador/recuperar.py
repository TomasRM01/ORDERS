# Programa que recupera las coordenadas de un .txt y genera un grafico

import random
import matplotlib.pyplot as plt
import re

# lista de posiciones
posiciones = []

# abrimos el fichero en modo lectura
f = open("scenary.txt", "r")    

# pasamos el contenido a un string
s = f.read()

# cerramos el fichero
f.close()

# desechamos todo lo que no son numeros y lo convertimos en una lista de elementos
s = [float(s) for s in re.findall(r'-?\d+\.?\d*', s)]

# para cada elemento de la lista, si es par lo guardamos en 'x' y si es impar, 
# lo guardamos en 'y' y agregamos la tupla a la lista de posiciones
for element in s:
    if s.index(element) % 2:
        y = element
        posiciones.append((x,y))
    else:
        x = element

# generamos el grafico
for t in posiciones:
    plt.scatter(t[0], t[1])
plt.title('Ciudades')
plt.xlabel('x')
plt.ylabel('y')
plt.savefig('scenary.png')
plt.show()