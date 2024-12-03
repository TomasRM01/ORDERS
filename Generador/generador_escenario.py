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
parser.add_argument("ruta_parametros_drones", type=str, help="Ruta del archivo donde se encuentran los parámetros para la generación de los drones.")  # Obligatorio
parser.add_argument("ruta_parametros_sensores", type=str, help="Ruta del archivo donde se encuentran los parámetros para la generación de los sensores.")  # Obligatorio
parser.add_argument("ruta_log", type=str, help="Ruta del archivo donde se escribirá el log.")  # Obligatorio
parser.add_argument("-s", "--seed", type=str, help="Semilla personalizada para la generación de los drones y sensores.")  # Opcional
args = parser.parse_args()

def main():
    
    # Recuperamos los parámetros de los drones y los sensores
    parametros_drones, parametros_sensores = recuperar_parametros()
    
    # Generamos la seed si no se ha especificado
    seed = args.seed
    if seed == None:
        # Generamos una semilla aleatoria en md5
        seed = generar_hash_aleatorio()
        
    print("Semilla: ", seed)
    
    # Escribimos la seed en el fichero
    try:
        f = abrirFichero(args.ruta_seed_escenario, 'w')
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    f.write(seed)
    f.close()
    
    # Generamos los drones y los sensores
    generaDrones(seed, args.ruta_drones, parametros_drones)
    generaSensores(seed, args.ruta_sensores, parametros_sensores)
    
    # Escribimos los parametros y la seed en el log
    escribir_log(seed, parametros_drones, parametros_sensores)
    

def generar_hash_aleatorio():
    # Generamos 16 bytes aleatorios (128 bits)
    bytes_aleatorios = os.urandom(16)
    # Convertimos los bytes aleatorios a una cadena hexadecimal
    hash_hex = hashlib.md5(bytes_aleatorios).hexdigest()
    return hash_hex

def recuperar_parametros():
    # Abrimos el archivo de parámetros de drones
    try:
        f = abrirFichero(args.ruta_parametros_drones, 'r')
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    
    # Leemos los parámetros de los drones
    parametros_drones = f.read().splitlines()
    f.close()
    
    # Abrimos el archivo de parámetros de sensores
    try:
        f = abrirFichero(args.ruta_parametros_sensores, 'r')
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    
    # Leemos los parámetros de los sensores
    parametros_sensores = f.read().splitlines()
    f.close()
    
    return parametros_drones, parametros_sensores

def escribir_log(seed, parametros_drones, parametros_sensores):
    try:
        f = abrirFichero(args.ruta_log, 'a')
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    
    f.write("Seed: " + seed + "\n\n")
    f.write("Parametros de drones:\n")
    for p in parametros_drones:
        f.write(p)
        f.write("\n")
    f.write("\n")
    f.write("Parametros de sensores:\n")
    for p in parametros_sensores:
        f.write(p)
        f.write("\n")
    
    # Escribimos el escenario generado
    f.write("\n")
    f.write("Drones generados:\n")
    try:
        fd = abrirFichero(args.ruta_drones, 'r')
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    f.write(fd.read())
    fd.close()
    
    f.write("\n")
    f.write("Sensores generados:\n")
    try:
        fs = abrirFichero(args.ruta_sensores, 'r')
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    f.write(fs.read())
    fs.close()
    
    f.write("\n\n\n")
    f.close()

main()