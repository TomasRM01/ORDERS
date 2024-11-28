import colorsys
from docplex.mp.model import Model
import time
import math
import re

from matplotlib import pyplot as plt
        
def main():
    
    # MODELO
    
    # Crear el modelo
    mdl = Model(name='ProblemaDrones')
    
    # DATOS
    
    # Extraer los datos del escenario
    peso_distancia, coordSensor, n, m, P, F, B, C, K, S, D, drones = extraerDatos()
    
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
    
    # Controlamos el caso en el que no se haya encontrado solucion
    if solution is None:
        print("No se ha encontrado solucion")
        print("Status = " + mdl.solve_details.status)
        return
    
    # Iteramos obteniendo los valores de las variables de decision y las guardamos en una matriz tridimensional
    x_sol = [[[0 for _ in range(n)] for _ in range(m)] for _ in range(m)]
    
    for i in range(m):
        for j in range(m):
            for k in range(n):
                x_sol[i][j][k] = solution.get_var_value(x[i,j,k])
    
    imprimirResultado(x_sol, solution, D, F, P, K, C, B, peso_distancia, n, m, coordSensor, mdl.solve_details)
    
    # guardamos en una variable cada camino de cada dron de la solucion
    caminos = []
    for k in K:
        camino = []
        i = 0
        j = 1
        while x_sol[i][0][k] == 0:
            if x_sol[i][j][k] == 1:
                camino.append((coordSensor[i]))
                i = j
                j = 1
            else:
                j += 1
        camino.append((coordSensor[i]))
        caminos.append(camino)
    
    dibujarCaminos(caminos, coordSensor, drones)

    
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
    
    return peso_distancia, coordSensor, n, m, P, F, B, C, K, S, D, drones

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

def imprimirResultado(x_sol, solution, D, F, P, K, C, B, peso_distancia, n, m, coordSensor, solve_details):
    
    string = ""
    string += f"{time.strftime('%d/%m/%Y, %H:%M:%S')}\n"
    string += "\n## RESULTADO ##\n\n"

    # Imprimir el fitness y el tiempo que ha tardado
    string += "Fitness = {:.2f}\n".format(solution.objective_value)
    string += "Tiempo = {:.2f}\n".format(solve_details.time)
    
    string += "\n"
    
    # Comprobamos si algun dron hace algun viaje
    seHacenViajes = False
    for k in K:
        if x_sol[0][0][k] != 1:
            seHacenViajes = True
            
    string += "Solucion encontrada\n"
    if seHacenViajes:
        if solution.is_feasible_solution():
            string += "La solucion es factible\n"
        else:
            string += "La solucion no es factible\n"
        string += "Status = " + solve_details.status + "\n"
    else:
        string += "Ningun dron hace ningun viaje\n"
        

    # Calcular la máxima prioridad posible
    maxPrioridad = sum(P)

    # Inicializar acumuladores
    maxDistancia = sum(C)
    maxRecarga = sum(B)

    sumaDistancias = 0
    sumaRecargas = 0
    sumaPrioridades = 0

    # Para cada dron
    for k in K:
        totalRecorrido = 0
        totalRecargado = 0
        totalPrioridad = 0
        
        string += f"\nDron {k + 1} (C = {C[k]:.2f}, B = {B[k]:.2f}):\n"
        
        # Comprobar si el dron no hace ningun viaje
        if x_sol[0][0][k] == 1:
            string += "- No hace ningun viaje\n"
        else:
            i = 0
            j = 1
            # Seguir su recorrido imprimiendo los caminos en orden
            while x_sol[i][0][k] == 0:
                if x_sol[i][j][k] == 1:
                    string += "- Viaja de " + str(i + 1) + " a " + str(j + 1) + " (D += {:.2f}, F += {:.2f}, P += {:.2f})\n".format(D[i][j], F[j], P[j])
                    totalRecorrido += D[i][j]
                    totalRecargado += F[j]
                    totalPrioridad += P[j]
                    i = j
                    j = 1
                else:
                    j += 1
            string += "- Viaja de " + str(i + 1) + " a 1 (D += {:.2f})\n".format(D[i][0])
            totalRecorrido += D[i][0]

            string += "- Total del dron (D = {:.2f}, F = {:.2f}, P = {:.2f})\n".format(totalRecorrido, totalRecargado, totalPrioridad)

        sumaDistancias += totalRecorrido
        sumaRecargas += totalRecargado
        sumaPrioridades += totalPrioridad

    # Calculamos los porcentajes controlando divisiones entre 0
    if maxDistancia > 0:
        porcentajeDistancia = (sumaDistancias / maxDistancia) * 100
    else:
        porcentajeDistancia = 100
    if maxRecarga > 0:
        porcentajeBateria = (sumaRecargas / maxRecarga) * 100
    else:
        porcentajeBateria = 100
    if maxPrioridad > 0:
        porcentajePrioridad = (sumaPrioridades / maxPrioridad) * 100
    else:
        porcentajePrioridad = 100
        
    # Resumen del resultado del problema
    string += "\n"
    string += "Distancia (D) = {:.2f} / {:.2f} ( {:.2f} % )\n".format(sumaDistancias, maxDistancia, porcentajeDistancia)
    string += "Bateria (F) = {:.2f} / {:.2f} ( {:.2f} % )\n".format(sumaRecargas, maxRecarga, porcentajeBateria)
    string += "Prioridad (P) = {:.2f} / {:.2f} ( {:.2f} % )\n".format(sumaPrioridades, maxPrioridad, porcentajePrioridad)

    string += "\n## PARAMETROS ##\n\n"

    # Imprimir los parámetros
    string += "Peso Distancia = " + str(peso_distancia) + "\n"

    string += "\n## ESCENARIO ##\n\n"

    # Imprimir el escenario inicial
    string += "- Semilla\n"
    string += str(open("Escenario/seed.txt", "r").read()) + "\n"
    string += "\n"
    string += "- Drones\n"
    string += "n = " + str(n) + "\n"
    string += "C = " + str(C) + "\n"
    string += "B = " + str(B) + "\n"
    string += "\n"
    string += "- Sensores\n"
    string += "m = " + str(m) + "\n"
    string += "coordSensor = " + str([(x, y) for [x, y] in coordSensor]) + "\n"
    string += "F = " + str(F) + "\n"
    string += "P = " + str(P) + "\n"
    string += "\n\n\n\n"

    print(string)
    
    f = open("CPLEX/Python/log_cplex_drones.txt", "a")
    f.write(string)
    f.close()

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

# Funcion auxiliar para generar un grafico que muestre los caminos de los drones
def dibujarCaminos(caminos, listaSensores, drones):
    
    nTotalSensores = 0
    nCaminos = 0
    listaColores = generarColoresUnicos(len(drones))
    
    for dron in caminos:
        nTotalSensores += len(dron) - 1
        x = []
        y = []
        for sensor in dron:
            x.append(sensor[0])
            y.append(sensor[1])
        x.append(dron[0][0])
        y.append(dron[0][1])
        plt.plot(x,y,":o",color=listaColores[nCaminos])
        nCaminos += 1
        
    # Obtenemos la lista de sensores no visitados por ningun dron comparando sus coordenadas
    sensoresNoVisitados = []
    for sensor in listaSensores:
        visitado = False
        for dron in caminos:
            for sensorDron in dron:
                if sensor[0] == sensorDron[0]:
                    visitado = True
                    break
        if not visitado:
            sensoresNoVisitados.append(sensor)
    
    # Imprimimos los sensores no visitados en gris
    x = []
    y = []
    for sensor in sensoresNoVisitados:
        x.append(sensor[0])
        y.append(sensor[1])
    plt.scatter(x, y, color='gray')
    
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
    plt.title('CPLEX')
    plt.text(caminos[0][0][0],caminos[0][0][1], " sensor origen")
    plt.show()

# Ejecutar el programa
main()