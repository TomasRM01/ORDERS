import colorsys
import random
import matplotlib.pyplot as plt

from gestor_ficheros import abrirFichero

def generaSensores(seed, ruta_sensores, parametros):

    # lista de posiciones, prioridades y baterias
    posiciones = []
    prioridades = []
    baterias = []
    
    # extraemos los parámetros
    num, max_x, max_y, max_p, max_b = recuperaParametros(parametros)

    random.seed(seed)
    
    try:
        f = abrirFichero(ruta_sensores, 'w')
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)

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
                    x = round(random.uniform(0, max_x), 2)
                    y = round(random.uniform(0, max_y), 2)
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

    # generamos el grafico
    colors = generarColoresUnicos(len(posiciones))

    for i, t in enumerate(posiciones):
        color = colors[i]
        plt.scatter(t[0], t[1], c=color)
        plt.annotate(f'P: {prioridades[i]}\nB: {baterias[i]}', (t[0], t[1]), textcoords="offset points", xytext=(0,-20), ha='center', fontsize=8)
    plt.title('Sensores')
    plt.xlabel('x')
    plt.ylabel('y')
    # plt.savefig('Escenario/scenary_sensores.png', dpi=300)
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

def recuperaParametros(parametros):

    num = int(parametros[0].split('=')[1].strip())
    max_x = int(parametros[1].split('=')[1].strip())
    max_y = int(parametros[2].split('=')[1].strip())
    max_p = int(parametros[3].split('=')[1].strip())
    max_b = int(parametros[4].split('=')[1].strip())
    
    return num, max_x, max_y, max_p, max_b