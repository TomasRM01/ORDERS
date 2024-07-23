from docplex.mp.model import Model
import math
import re
        

def main():
    
    # MODELO
    
    # Crear el modelo
    mdl = Model(name='ProblemaDrones')
    
    # DATOS
    
    # Extraer los datos del escenario
    peso_distancia, n, m, P, F, B, C, K, S, D = extraerDatos()
    
    # VARIABLES
    
    # Definimos las variables de decision
    x = mdl.binary_var_cube(m, m, n, name='x')
    u = mdl.integer_var_list(m, lb=1, ub=m, name='u')
    
    # FUNCION OBJETIVO

    # Función Objetivo
    mdl.maximize(mdl.sum(x[i, j, k] * P[j] for i in S for j in S for k in K) - peso_distancia * mdl.sum(x[i, j, k] * D[i][j] for i in S for j in S for k in K))

    # RESTRICCIONES
    
    # Creamos las restricciones
    crearRestricciones(mdl, m, x, u, S, K, D, C, F, B)

    # RESOLVER
    
    # Resolver el modelo
    solution = mdl.solve()

    # RESULTADOS

    # Verificar y obtener la solución
    if solution:
        print("Solution status: ", solution.solve_status)
        print("Objective value: ", solution.objective_value)
        print("Time: ", solution.solve_details.time)
        # for var in mdl.iter_variables():
        #     print(f"{var.name}: {var.solution_value}")
    else:
        print("No solution found")
        
def extraerDatos():
    
    peso_distancia = 0.001
    
    drones = recuperaDrones()
    sensores = recuperaSensores()
    n = len(drones)
    m = len(sensores)
    coordSensor = [[s[0][0], s[0][1]] for s in sensores]
    P = [s[1] for s in sensores]
    F = [s[2] for s in sensores]
    B = [d['battery_capacity'] for d in drones]
    C = [d['distance_capacity'] for d in drones]
    

    # Sets
    K = range(n) # Drones
    S = range(m) # Sensores

    # Calcular la matriz de distancias
    D = [[0]*m for _ in range(m)]
    for i in S:
        for j in S:
            if i != j:
                D[i][j] = math.sqrt((coordSensor[i][0] - coordSensor[j][0])**2 + (coordSensor[i][1] - coordSensor[j][1])**2)

    # Ajustes para el punto inicial
    F[0] = 0
    P[0] = 0
    
    return peso_distancia, n, m, P, F, B, C, K, S, D

def crearRestricciones(mdl, m, x, u, S, K, D, C, F, B):
    
    # El destino debe ser distinto al origen, excepto para el inicial
    for i in S:
        if i > 0:
            for k in K:
                mdl.add_constraint(x[i, i, k] == 0, f'destino_distinto_sensor_{i}_{k}')

    # Los drones deben partir y regresar al origen
    for k in K:
        mdl.add_constraint(mdl.sum(x[i, 0, k] for i in S) == 1, f'partida_inicio_{k}')
        mdl.add_constraint(mdl.sum(x[0, i, k] for i in S) == 1, f'regreso_inicio_{k}')

    # Cada sensor es visitado por 0 o 1 drones, excepto el inicial
    for i in S:
        if i > 0:
            for j in S:
                mdl.add_constraint(mdl.sum(x[i, j, k] for k in K) <= 1, f'sensor_visitado_por_un_dron_{i}_{j}')

    # Desde cada sensor solo puede partir un dron, excepto desde el inicial
    for i in S:
        if i > 0:
            mdl.add_constraint(mdl.sum(x[i, j, k] for j in S for k in K) <= 1, f'solo_sale_uno_{i}')

    # A un sensor solo puede llegar un dron, excepto para el inicial
    for j in S:
        if j > 0:
            mdl.add_constraint(mdl.sum(x[i, j, k] for i in S for k in K) <= 1, f'solo_llega_uno_{j}')

    # Si un dron va de i a j, debe existir un sensor i2 desde el que se parte hasta i
    for i in S:
        if i > 0:
            for j in S:
                for k in K:
                    mdl.add_constraint(x[i, j, k] <= mdl.sum(x[i2, i, k] for i2 in S), f'debe_ser_visitado_previamente_{i}_{j}_{k}')

    # Eliminación de subrutas utilizando MTZ (orden de visita de sensores)
    for i in S:
        for j in S:
            if i != j and j != 0:
                for k in K:
                    mdl.add_constraint(u[i] + 1 <= u[j] + m * (1 - x[i, j, k]), f'elimina_subrutas_{i}_{j}_{k}')

    # Restricciones para que los valores del vector de orden de subrutas estén dentro de unos límites
    for i in S:
        if i > 0:
            mdl.add_constraint(1 <= u[i], f'limite_inferior_{i}')
            mdl.add_constraint(u[i] <= m - 1, f'limite_superior_{i}')

    # El sensor inicial siempre se visita primero
    mdl.add_constraint(u[0] == 1, 'sensor_inicial_primero')

    # Nos aseguramos que el orden de los valores del vector de visita sea secuencial
    for i in S:
        for j in S:
            if j > 0:
                for k in K:
                    mdl.add_constraint((x[i, j, k] != 1) | (u[i] + 1 == u[j]), f'orden_de_visita_secuencial_{i}_{j}_{k}')

    # Restricciones del estilo KP
    # La distancia recorrida por un dron debe ser menor o igual a la distancia máxima que puede recorrer
    for k in K:
        mdl.add_constraint(mdl.sum(x[i, j, k] * D[i][j] for i in S for j in S) <= C[k], f'distancia_{k}')

    # La batería recargada por un dron debe ser menor o igual a la batería máxima que puede recargar
    for k in K:
        mdl.add_constraint(mdl.sum(x[i, j, k] * F[j] for i in S for j in S) <= B[k], f'recarga_{k}')

# Funcion que lee el contenido de el fichero scenary_drones.txt y devuelve la lista de drones con sus capacidades
def recuperaDrones():
    # lista de drones
    drones = []

    # abrimos el fichero en modo lectura
    with open("Escenario/scenary_drones.txt", "r") as f:
        # pasamos el contenido a un string
        s = f.read()
        
    # recuperamos los elementos del string tal que asi: {'distance_capacity': 137, 'battery_capacity': 1158}, {'distance_capacity': 108, 'battery_capacity': 1690}, ...
    drones = [eval(drone) for drone in re.findall(r'\{.*?\}', s)]

    # cerramos el fichero
    f.close()
    
    return drones

# Funcion que lee el contenido de el fichero scenary_sensores.txt y devuelve la lista de sensores con sus coordenadas
def recuperaSensores():
    
    # lista de sensores
    sensores = []

    # abrimos el fichero en modo lectura
    with open("Escenario/scenary_sensores.txt", "r") as f:
        # pasamos el contenido a un string
        s = f.read()

    # desechamos todo lo que no son numeros y lo convertimos en una lista de elementos
    s = [float(s) for s in re.findall(r'\d+\.?\d*', s)]

    # guardamos los elementos en las listas correspondientes
    for i in range(0, len(s), 4):
        x = s[i]
        y = s[i+1]
        p = s[i+2]
        b = s[i+3]
        sensores.append(((x, y), p, b))

    return sensores

# Ejecutar el programa
main()