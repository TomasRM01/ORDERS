from docplex.mp.model import Model
import math

# Leer los datos desde los archivos .dat
def read_dat_file(filepath):
    data = {}
    with open(filepath, 'r') as file:
        exec(file.read(), data)
    return data

# Leer los archivos .dat
data_files = ["CPLEX/Python/Drones.dat", "CPLEX/Python/Parametros.dat", "CPLEX/Python/Sensores.dat"]
data = {}
for data_file in data_files:
    data.update(read_dat_file(data_file))

# Variables leídas de los archivos .dat
n = data['n']
m = data['m']
peso_distancia = data['peso_distancia']
coordSensor = data['coordSensor']
F = data['F']
P = data['P']
B = data['B']
C = data['C']

# Crear el modelo
mdl = Model(name='ProblemaDrones')

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

# Definir las variables de decisión
x = mdl.binary_var_cube(m, m, n, name='x')
u = mdl.integer_var_list(m, lb=1, ub=m, name='u')

# Función Objetivo
mdl.maximize(mdl.sum(x[i, j, k] * P[j] for i in S for j in S for k in K) - peso_distancia * mdl.sum(x[i, j, k] * D[i][j] for i in S for j in S for k in K))

# Restricciones
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


# Resolver el modelo
solution = mdl.solve()

# Verificar y obtener la solución
if solution:
    print("Solution status: ", solution.solve_status)
    print("Objective value: ", solution.objective_value)
    # for var in mdl.iter_variables():
    #     print(f"{var.name}: {var.solution_value}")
else:
    print("No solution found")
