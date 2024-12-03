import random

from gestor_ficheros import abrirFichero

def generaDrones(seed, ruta_drones, parametros):
    
    # Extraemos los parámetros
    num_drones, min_distance, max_distance, min_battery, max_battery = recuperaParametros(parametros)

    # Definimos las listas donde se almacenaran las capacidades de los drones
    B = []
    C = []
    n = 0

    try:
        f = abrirFichero(ruta_drones, 'w')
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)

    random.seed(seed)

    for _ in range(num_drones):
        n += 1
        B.append(random.randint(min_battery, max_battery))
        C.append(random.randint(min_distance, max_distance))
        dron = {
            'dron_n': n,  # drone number
            'battery_capacity': B[n - 1],  # battery capacity variable
            'distance_capacity': C[n - 1]  # distance capacity variable
        }
        f.write(str(dron) + '\n')
        
    f.close()
    
def recuperaParametros(parametros):

    num_drones = int(parametros[0].split('=')[1].strip())
    min_distance = int(parametros[1].split('=')[1].strip())
    max_distance = int(parametros[2].split('=')[1].strip())
    min_battery = int(parametros[3].split('=')[1].strip())
    max_battery = int(parametros[4].split('=')[1].strip())
    
    return num_drones, min_distance, max_distance, min_battery, max_battery