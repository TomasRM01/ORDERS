import colorsys
import random
import matplotlib.pyplot as plt

def generaSensores(seed):

    # numero de sensores
    num = 20

    # coordenadas maximas
    max_x = 100
    max_y = 100

    # prioridad maxima
    max_p = 10

    # bateria faltante maxima
    max_b = 200

    # lista de posiciones, prioridades y baterias
    posiciones = []
    prioridades = []
    baterias = []

    # abrimos el fichero en modo escritura
    f = open("Escenario/scenary_sensores.txt", "w")
    
    random.seed(seed)

    # iteramos para num sensores
    for _ in range(num):
        
        # generamos coordenadas aleatorias
        x = round(random.uniform(0, max_x), 2)
        y = round(random.uniform(0, max_y), 2)
        
        # evitamos dos ciudades demasiado juntas
        repetido = 1
        while repetido == 1:
            repetido = 0
            for t in posiciones:
                if (abs(t[0] - x) <= 3 and abs(t[1] - y) <= 3):
                    repetido = 1
                    x = round(random.uniform(0, 100), 2)
                    y = round(random.uniform(0, 100), 2)
                    break
        
        # generamos una prioridad aleatoria
        prioridad = random.randint(0, max_p)
        
        # generamos una bateria faltante aleatoria
        bateria = random.randint(0, max_b)
        
        # añadimos las posiciones, prioridades y baterias a los vectores
        posiciones.append((x, y))
        prioridades.append(prioridad)
        baterias.append(bateria)
        
        # añadimos la linea al fichero
        string = "X: {:05.2f}\tY: {:05.2f}\tP: {}\tB: {}\n".format(x, y, prioridad, bateria)
        f.write(string)

    # cerramos el fichero
    f.close()

    # ! Solo se usa para el editor externo de CPLEX Studio
    # # Fichero de salida para CPLEX
    # f2 = open("CPLEX/Drones/Sensores.dat", "w")

    # f2.write('// Numero de sensores' + '\n' + 'm = ' + str(num) + ';\n')
    # f2.write('// Coordenadas de los sensores' + '\n' + 'coordSensor = ' + str([f'<{x:.2f}, {y:.2f}>' for x, y in posiciones]).replace("'", "") + ';\n')
    # f2.write('// Prioridades' + '\n' + 'P = ' + str(prioridades) + ';\n')
    # f2.write('// Carga necesaria' + '\n' + 'F = ' + str(baterias) + ';\n')

    # f2.close()
    # ! Solo se usa para el editor externo de CPLEX Studio

    # generamos el grafico
    colors = generarColoresUnicos(len(posiciones))

    for i, t in enumerate(posiciones):
        color = colors[i]
        plt.scatter(t[0], t[1], c=color)
        plt.annotate(f'P: {prioridades[i]}\nB: {baterias[i]}', (t[0], t[1]), textcoords="offset points", xytext=(0,-20), ha='center', fontsize=8)
    plt.title('Sensores')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig('Escenario/scenary_sensores.png', dpi=300)
    print("Mostrando sensores. Cierre la ventana para finalizar.")
    plt.show()

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