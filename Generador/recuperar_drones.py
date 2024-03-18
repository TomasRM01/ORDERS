# Programa que recupera los drones que se van a utilizar en el escenario.

import matplotlib.pyplot as plt
import re

# lista de drones
drones = []

# abrimos el fichero en modo lectura
with open("scenary_drones.txt", "r") as f:
    # pasamos el contenido a un string
    s = f.read()
    
# recuperamos los elementos del string tal que asi: {'distance_capacity': 137, 'battery_capacity': 1158}, {'distance_capacity': 108, 'battery_capacity': 1690}, ...
drones = [eval(drone) for drone in re.findall(r'\{.*?\}', s)]

# imprimimos los drones+
for dron in drones:
    print(dron)

# cerramos el fichero
f.close()