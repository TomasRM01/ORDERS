import time
import copy
import re
import colorsys
import matplotlib.pyplot as plt
from genetico_drones import startGenetico
from aux_genetico_drones import distanciaTotalDron, prioridadTotalDron, bateriaTotalDron, distanciaEuclidea

def main():
    
    resultados = []

    n_ejecuciones = 31

    # Variables importantes configurables para el algoritmo genetico
    peso_distancia = 0.001
    tamano_poblacion = 200
    porcentaje_mejor = 10
    probabilidad_cruce = 90
    probabilidad_mutante = 1
    maximo_generaciones_sin_mejora = 10

    # Recuperamos los drones del .txt
    drones = recuperaDrones()
        
    # Recuperamos los sensores del .txt
    listaSensores = recuperaSensores()

    for _ in range(n_ejecuciones):
        
        # Imprimimos el progreso de las ejecuciones 
        printProgressBar(_, n_ejecuciones - 1, prefix = 'Progreso:', suffix = 'Completado', length = 50)
        
        # Ejecutamos el algoritmo genético con los parámetros configurados
        solucion = startGenetico(peso_distancia, tamano_poblacion, porcentaje_mejor, probabilidad_cruce, probabilidad_mutante, maximo_generaciones_sin_mejora, drones, listaSensores)
        
        # TODO: Comprobar que la solucion cumple con las restricciones (valores dentro de lo esperado, que no haya subrutas)
        # TODO: Si alguna solucion no es correcta o su fitness es inferior al de la solucion exacta, paramos la ejecucion
        
        # Guardamos la solución obtenida en la lista de resultados
        resultados.append(solucion)
    

    # Ordenamos los resultados por valor fitness
    resultados.sort(key=lambda x: x[1])

    # Obtenemos el índice central de la lista de resultados
    middle_index = len(resultados) // 2

    # Obtenemos la solución central
    solucion_central = resultados[middle_index]
    
    # Escribimos los resultados obtenidos por el algoritmo genético en un fichero de log
    escribirResultados(solucion_central, tamano_poblacion, porcentaje_mejor, probabilidad_cruce, probabilidad_mutante, maximo_generaciones_sin_mejora, solucion_central[2], drones, peso_distancia, listaSensores)
    
    # Dibujamos los caminos de la solución central
    dibujarCaminos(solucion_central, listaSensores, drones)
    


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
def dibujarCaminos(mejorSolucion, listaSensores, drones):
    
    nTotalSensores = 0
    nCaminos = 0
    listaColores = generarColoresUnicos(len(drones))
    
    for dron in mejorSolucion[0]:
        nTotalSensores += len(dron) - 1
        x = []
        y = []
        for sensor in dron:
            x.append(sensor[0][0])
            y.append(sensor[0][1])
        x.append(dron[0][0][0])
        y.append(dron[0][0][1])
        plt.plot(x,y,":o",color=listaColores[nCaminos])
        nCaminos += 1
        
    # Obtenemos la lista de sensores no visitados por ningun dron comparando sus coordenadas
    sensoresNoVisitados = []
    for sensor in listaSensores:
        visitado = False
        for dron in mejorSolucion[0]:
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
        x.append(sensor[0][0])
        y.append(sensor[0][1])
    plt.scatter(x, y, color='gray')
    
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
    plt.title('Gráfico de Caminos')
    plt.text(mejorSolucion[0][0][0][0][0],mejorSolucion[0][0][0][0][1], " sensor origen")
    plt.show()


# Funcion auxiliar que escribe los resultados obtenidos por el algoritmo genetico en un fichero de log y por pantalla
def escribirResultados(mejorSolucion, tamano_poblacion, porcentaje_mejor, probabilidad_cruce, probabilidad_mutante, maximo_generaciones_sin_mejora, tiempo_total, drones, peso_distancia, listaSensores):
    
    copiaListaSensores = copy.deepcopy(listaSensores)
    
    # Establecemos a 0 la prioridad y la bateria del sensor de origen
    # Se hace para que al imprimir el escenario se vea que el sensor de origen tiene prioridad y bateria 0
    copiaListaSensores[0] = (copiaListaSensores[0][0], 0, 0)
    
    # Calculamos la distancia total, la bateria recargada y la prioridad acumulada por los drones
    distanciaTotal = 0
    bateriaTotal = 0
    prioridadTotal = 0
    resultadosDrones = []
    for i, dron in enumerate(mejorSolucion[0]):
        # Calculamos la distancia, prioridad y bateria total
        distanciaDron = distanciaTotalDron(dron)
        distanciaTotal += distanciaDron
        prioridadDron = prioridadTotalDron(dron)
        prioridadTotal += prioridadDron
        bateriaDron = bateriaTotalDron(dron)
        bateriaTotal += bateriaDron
        
        # Generamos el resultado del dron
        resultadoDron = f"\nDron {i+1} (C = {drones[i]['distance_capacity']:.2f}, B = {drones[i]['battery_capacity']:.2f}):"
        
        if len(dron) == 1:
            resultadoDron += f"\n- No hace ningun viaje"
        else:
            # recorremos los sensores del camino hasta el penultimo
            for j, sensor in enumerate(dron[:-1]):
                # Buscamos en la lista de sensores el index de los sensores con las mismas coordenadas que los sensores del camino
                # solo miramos las coordenadas, ya que la prioridad y la bateria de los sensores pueden diferir
                origen = copiaListaSensores.index([s for s in copiaListaSensores if s[0] == sensor[0]][0])
                destino = copiaListaSensores.index([s for s in copiaListaSensores if s[0] == dron[j+1][0]][0])
                resultadoDron += f"\n- Viaja de {origen + 1} a {destino + 1} (D += {distanciaEuclidea(sensor[0],dron[j+1][0]):.2f}, F += {dron[j+1][2]:.2f}, P += {dron[j+1][1]:.2f})"
            # Incluimos el regreso al sensor de origen
            origen = copiaListaSensores.index([s for s in copiaListaSensores if s[0] == dron[-1][0]][0])
            destino = copiaListaSensores.index([s for s in copiaListaSensores if s[0] == dron[0][0]][0])
            resultadoDron += f"\n- Viaja de {origen + 1} a {destino + 1} (D += {distanciaEuclidea(dron[-1][0],dron[0][0]):.2f})"
            resultadoDron += f"\n- Total del dron (D = {distanciaDron:.2f}, F = {bateriaDron:.2f}, P = {prioridadDron:.2f})"
        
        resultadosDrones.append(resultadoDron)
    
    # Calculamos la distancia maxima y bateria maxima recargable por los drones
    distanciaMaxima = sum(dron['distance_capacity'] for dron in drones)
    bateriaMaxima = sum(dron['battery_capacity'] for dron in drones)
    
    # Calculamos la prioridad maxima acumulable por los drones (sin contar el sensor de origen)  
    prioridadMaxima = sum(sensor[1] for sensor in copiaListaSensores[1:])
    
    # Calculamos los porcentajes de distancia, bateria y prioridad, evitando divisiones entre 0
    if distanciaMaxima > 0:
        porcentajeDistancia = (distanciaTotal / distanciaMaxima) * 100
    else:
        porcentajeDistancia = 100
    if bateriaMaxima > 0:
        porcentajeBateria = (bateriaTotal / bateriaMaxima) * 100
    else:
        porcentajeBateria = 100
    if prioridadMaxima > 0:
        porcentajePrioridad = (prioridadTotal / prioridadMaxima) * 100
    else:
        porcentajePrioridad = 100
    
    # Escribimos en el fichero de log los resultados obtenidos por el algoritmo genetico y cerramos el fichero
    f = open("Genetico/log_drones_genetico.txt", "a")
    string = f"{time.strftime('%d/%m/%Y, %H:%M:%S')}"
    string += "\n\n## RESULTADO ##" 
    string += f"\n\nFitness = {mejorSolucion[1]:.2f}"
    string += f"\nTiempo = {tiempo_total:.2f}"
    string += "\n" + "\n".join(resultadosDrones)
    string += f"\n\nDistancia (D) = {distanciaTotal:.2f} / {distanciaMaxima:.2f} ( {porcentajeDistancia:.2f}% )"
    string += f"\nBateria   (F) = {bateriaTotal:.2f} / {bateriaMaxima:.2f} ( {porcentajeBateria:.2f}% )"
    string += f"\nPrioridad (P) = {prioridadTotal:.2f} / {prioridadMaxima:.2f} ( {porcentajePrioridad:.2f}% )"
    string += "\n\n## PARAMETROS ##"
    string += f"\n\nPeso Distancia = {peso_distancia}"
    string += f"\nTamano Poblacion = {tamano_poblacion}"
    string += f"\nPorcentaje Mejor = {porcentaje_mejor}"
    string += f"\nProbabilidad Cruce = {probabilidad_cruce}"
    string += f"\nProbabilidad Mutante = {probabilidad_mutante}"
    string += f"\nMaximo Generaciones sin Mejora = {maximo_generaciones_sin_mejora}"
    string += "\n\n## ESCENARIO ##"
    string += f"\n\n- Drones\nn = {len(drones)}\nC = [{', '.join(str(dron['distance_capacity']) for dron in drones)}]\nB = [{', '.join(str(dron['battery_capacity']) for dron in drones)}]"
    string += f"\n\n- Sensores\nm = {len(copiaListaSensores)}\ncoordSensor = [{', '.join(str(sensor[0]) for sensor in copiaListaSensores)}]\nF = [{', '.join(str(sensor[2]) for sensor in copiaListaSensores)}]\nP = [{', '.join(str(sensor[1]) for sensor in copiaListaSensores)}]"
    string += "\n\n\n\n\n"
    f.write(string)
    f.close()
    
    # Imprimimos lo mismo por pantalla
    print(string)
    
# Print iterations progress (fuente: https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters)
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print("\n")
    
# Ejecutamos la funcion main
main()