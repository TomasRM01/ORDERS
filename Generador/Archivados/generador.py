# Programa que genera un escenario inicial

import random
import matplotlib.pyplot as plt

# abrimos el fichero en modo escritura
f = open("scenary.txt", "w")

# numero de ciudades
num = 100

# lista de posiciones
posiciones = []

# iteramos para num ciudades
for _ in range(num):
    
    # generamos coordenadas aleatorias
    x = round(random.uniform(0, 100), 2)
    y = round(random.uniform(0, 100), 2)
    
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
    
    # añadimos las posiciones al vector
    posiciones.append((x, y))
    
    # añadimos la linea al fichero
    string = "X: {:05.2f}\tY: {:05.2f}\n".format(x, y)
    f.write(string)

# cerramos el fichero
f.close()

# generamos el grafico
for t in posiciones:
    plt.scatter(t[0], t[1])
plt.title('Ciudades')
plt.xlabel('x')
plt.ylabel('y')
plt.savefig('scenary.png')
plt.show()

