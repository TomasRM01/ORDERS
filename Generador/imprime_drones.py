#!/usr/bin/env python3

# Programa que recupera los drones que se van a utilizar en el escenario.

import re
import argparse

from gestor_ficheros import abrirFichero

# Crear un parser para manejar los argumentos
parser = argparse.ArgumentParser(description="Programa que imprime por pantalla los parámetros de los drones del escenario.")
parser.add_argument("ruta_drones", type=str, help="Ruta del archivo que contiene los parámetros de los drones.")  # Obligatorio
args = parser.parse_args()

# lista de drones
drones = []

# abrimos el fichero en modo lectura
try:
    f = abrirFichero(args.ruta_drones, 'r')
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit(1)
    
# pasamos el contenido a un string
s = f.read()
    
# recuperamos los elementos del string tal que asi: {'distance_capacity': 137, 'battery_capacity': 1158}, {'distance_capacity': 108, 'battery_capacity': 1690}, ...
drones = [eval(drone) for drone in re.findall(r'\{.*?\}', s)]

# imprimimos los drones+
for dron in drones:
    print(dron)

# cerramos el fichero
f.close()