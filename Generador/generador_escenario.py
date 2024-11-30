#!/usr/bin/env python3

import os
import hashlib
import argparse

from gestor_ficheros import abrirFichero
from generador_drones import generaDrones
from generador_sensores import generaSensores

# Crear un parser para manejar los argumentos
parser = argparse.ArgumentParser(description="Programa que genera los drones y sensores de un escenario.")
parser.add_argument("ruta_drones", type=str, help="Ruta del archivo donde se escribirán los parámetros de los drones.")  # Obligatorio
parser.add_argument("ruta_sensores", type=str, help="Ruta del archivo donde se escribirán los parámetros de los sensores.")  # Obligatorio
parser.add_argument("ruta_seed_escenario", type=str, help="Ruta del archivo donde se escribirá la seed del escenario.")  # Obligatorio
parser.add_argument("-s", "--seed", type=str, help="Semilla personalizada para la generación de los drones y sensores.")  # Opcional
args = parser.parse_args()

def main():
    
    seed = args.seed
    if seed == None or seed == "":
        # Generamos una semilla aleatoria en md5
        seed = generar_hash_aleatorio()
        
    print("Semilla: ", seed)
    
    try:
        f = abrirFichero(args.ruta_seed_escenario, 'w')
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    f.write(seed)
    f.close()
    
    generaDrones(seed, args.ruta_drones)
    generaSensores(seed, args.ruta_sensores)

def generar_hash_aleatorio():
    # Generamos 16 bytes aleatorios (128 bits)
    bytes_aleatorios = os.urandom(16)
    # Convertimos los bytes aleatorios a una cadena hexadecimal
    hash_hex = hashlib.md5(bytes_aleatorios).hexdigest()
    return hash_hex

main()