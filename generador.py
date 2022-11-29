# This program prints Hello, world!

import random

f = open("scenary.txt", "w")

num = 100

posiciones = []

for _ in range(num):
    
    x = round(random.uniform(0, 100), 2)
    y = round(random.uniform(0, 100), 2)
    
    repetido = 0
    while repetido == 1:
        repetido = 0
        for t in posiciones:
            if t == (x,y):
                print("Repetido")
                repetido = 1
                x = round(random.uniform(0, 100), 2)
                y = round(random.uniform(0, 100), 2)
                break
            
    posiciones.append((x, y))
    
    string = "X: {:05.2f}\tY: {:05.2f}\n".format(x, y)
    
    f.write(string)

f.close()

#open and read the file after the appending:
# f = open("scenary.txt", "r")
# print(f.read())