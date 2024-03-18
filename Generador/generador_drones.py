# Programa que genera un fichero con los drones que se van a utilizar en el escenario.

import random

# abrimos el fichero en modo escritura
f = open("scenary_drones.txt", "w")

# definimos el numero de drones, en este caso 3
num_drones = 3
    
# Definimos los valores minimos y maximos para las capacidades de los drones
min_distance = 100
max_distance = 150
min_battery = 1000
max_battery = 2500

for _ in range(num_drones):
    dron = {
        'distance_capacity': random.randint(min_distance, max_distance),  # distance capacity variable
        'battery_capacity': random.randint(min_battery, max_battery)  # battery capacity variable
    }
    f.write(str(dron) + '\n')
    
f.close()