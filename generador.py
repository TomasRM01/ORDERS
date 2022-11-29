# This program prints Hello, world!

import random

f = open("scenary.txt", "w")

num = 100
for _ in range(num):
    string = "X: {}\tY: {}\n".format(round(random.uniform(0, 100), 2), round(random.uniform(0, 100), 2))
    f.write(string)

f.close()

#open and read the file after the appending:
f = open("scenary.txt", "r")
print(f.read())