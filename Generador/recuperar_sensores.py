import matplotlib.pyplot as plt
import re
import random

# lista de posiciones, prioridades y baterias
posiciones = []
prioridades = []
baterias = []

# abrimos el fichero en modo lectura
with open("scenary_sensores.txt", "r") as f:
    # pasamos el contenido a un string
    s = f.read()

# desechamos todo lo que no son numeros y lo convertimos en una lista de elementos
s = [float(s) for s in re.findall(r'\d+\.?\d*', s)]

# guardamos los elementos en las listas correspondientes
contador = 0
for i in range(0, len(s), 4):
    x = s[i]
    y = s[i+1]
    p = s[i+2]
    b = s[i+3]
    posiciones.append((x, y))
    prioridades.append(p)
    baterias.append(b)

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
