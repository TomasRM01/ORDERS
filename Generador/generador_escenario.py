#!/usr/bin/env python3

from generador_drones import generaDrones
from generador_sensores import generaSensores

import os
import hashlib

def main():
    
    # Pedimos la semilla o la generamos aleatoriamente
    seed = input("Introduce una semilla o pulsa enter para generar una aleatoria: ")
    
    if seed == "":
        # Generamos una semilla aleatoria en md5
        seed = generar_hash_aleatorio()
        
    print("Semilla: ", seed)
    
    # Guardamos la semilla en un fichero
    f = open("Escenario/seed.txt", "w")
    f.write(seed)
    f.close()
    
    generaDrones(seed)
    generaSensores(seed)

def generar_hash_aleatorio():
    # Generamos 16 bytes aleatorios (128 bits)
    bytes_aleatorios = os.urandom(16)
    # Convertimos los bytes aleatorios a una cadena hexadecimal
    hash_hex = hashlib.md5(bytes_aleatorios).hexdigest()
    return hash_hex

main()