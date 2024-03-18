import random
import matplotlib.pyplot as plt

# abrimos el fichero en modo escritura
f = open("scenary_sensores.txt", "w")

# numero de sensores
num = 100

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

# generamos el grafico
colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'gray', 'cyan']
for i, t in enumerate(posiciones):
    color = random.choice(colors)
    plt.scatter(t[0], t[1], c=color)
    plt.annotate(f'P: {prioridades[i]}\nB: {baterias[i]}', (t[0], t[1]), textcoords="offset points", xytext=(0,-20), ha='center', fontsize=8)
plt.title('Sensores')
plt.xlabel('x')
plt.ylabel('y')
plt.savefig('scenary_sensores.png', dpi=300)
plt.show()

