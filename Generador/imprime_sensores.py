#!/usr/bin/env python3

# Programa que recupera los sensores que se van a utilizar en el escenario.

import re
import colorsys
import matplotlib.pyplot as plt
import argparse

from gestor_ficheros import abrirFichero

# Crear un parser para manejar los argumentos
parser = argparse.ArgumentParser(description="Programa que imprime por pantalla los parámetros de los sensores del escenario.")
parser.add_argument("ruta_sensores", type=str, help="Ruta del archivo que contiene los parámetros de los sensores.")  # Obligatorio
args = parser.parse_args()

# lista de posiciones, prioridades y baterias
posiciones = []
prioridades = []
baterias = []

# abrimos el fichero en modo lectura
try:
    f = abrirFichero(args.ruta_sensores, 'r')
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit(1)
    
# pasamos el contenido a un string
s = f.read()

print(s)

# desechamos todo lo que no son numeros y lo convertimos en una lista de elementos
s = [float(s) for s in re.findall(r'\d+\.?\d*', s)]

# guardamos los elementos en las listas correspondientes
for i in range(0, len(s), 4):
    x = s[i]
    y = s[i+1]
    p = s[i+2]
    b = s[i+3]
    posiciones.append((x, y))
    prioridades.append(p)
    baterias.append(b)
    
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

# generamos el grafico
colors = generarColoresUnicos(len(posiciones))

for i, t in enumerate(posiciones):
    color = colors[i]
    plt.scatter(t[0], t[1], c=color)
    plt.annotate(f'P: {prioridades[i]}\nB: {baterias[i]}', (t[0], t[1]), textcoords="offset points", xytext=(0,-20), ha='center', fontsize=8)
plt.title('Sensores')
plt.xlabel('x')
plt.ylabel('y')
# plt.savefig('Escenario/scenary_sensores.png', dpi=300)
print("Mostrando sensores. Cierre la ventana para finalizar.")
plt.show()