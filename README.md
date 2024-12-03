# Optimización de Rutas para Drones En Redes de Sensores (ORDERS)
## Instrucciones para clonar el repositorio

Para clonar el repositorio, ejecute el siguiente comando en su terminal:

```bash
git clone https://github.com/TomasRM01/ORDERS.git
```

## Instalación de dependencias

Se requiere el uso de la versión 3.10 de Python. Puedes descargarla en el siguiente enlace: [Python 3.10.11](https://www.python.org/downloads/release/python-31011/). Para el desarrollo y testeo de este proyecto, se utilizó la versión 3.10.11 de Python.

Navegue al directorio del proyecto y ejecute el siguiente comando para instalar las dependencias necesarias:

```bash
pip install matplotlib
```

Para usar el resolutor de CPLEX, es necesario tener instalado IBM ILOG CPLEX Optimization Studio. Puede descargar una versión gratuita académica en el siguiente enlace: [IBM ILOG CPLEX Optimization Studio](https://academic.ibm.com/a2mt/downloads/data_science#/) (Debes registrarte con tu correo institucional para poder descargar la versión gratuita).

Una vez instalado, para configurar CPLEX con Python, navegue a la carpeta de instalación de CPLEX y ejecute el siguiente comando como administrador:

```bash
cd IBM\ILOG\CPLEX_Studio2211\python
python3 setup.py install
```

Para terminar, instalamos docplex. Este no soporta numpy 2.0.1, por lo que se debe instalar una version anterior:

```bash
pip install docplex numpy<2.0
```
### Opción sin licencia de CPLEX
Si no tiene acceso a la versión completa de CPLEX, puede utilizar la versión gratuita de docplex, que tiene limitaciones en la cantidad de variables y restricciones que se pueden utilizar. Para ello, ejecute el siguiente comando:

```bash
pip install cplex
```

## Estructura de archivos
La estructura del proyecto es la siguiente:

```
ORDERS/
├── CPLEX/
│   ├── cplex_drones.py
│   ├── gestor_ficheros.py
│   └── ...
├── Escenario/
│   └── ...
├── Generador/
│   ├── generador_drones.py
│   ├── generador_escenario.py
│   ├── generador_sensores.py
│   ├── gestor_ficheros.py
│   ├── imprime_sensores.py
│   └── ...
├── Genetico/
│   ├── aux_genetico_drones.py
│   ├── genetico_drones.py
│   ├── gestor_ficheros.py
│   ├── main_genetico_drones.py
│   └── ...
└── README.md
```

- `CPLEX/`: Contiene los scripts necesarios para utilizar el método de resolución exacto.
    - `cplex_drones.py`: Script principal para ejecutar el método de resolución exacto.
    - `gestor_ficheros.py`: Contiene funciones para leer y escribir archivos.
- `Escenario/`: Contiene los parametros de los drones, sensores y semilla.
- `Generador/`: Contiene los scripts necesarios para generar escenarios.
    - `generador_drones.py`: Script que contiene el código necesario para generar drones.
    - `generador_escenario.py`: Este script genera un escenario con drones y sensores utilizando generador_drones.py y generador_sensores.py.
    - `generador_sensores.py`: Script que contiene el código necesario para generar sensores.
    - `gestor_ficheros.py`: Contiene funciones para leer y escribir archivos.
    - `imprime_sensores.py`: Script que imprime los sensores del escenario y los representa gráficamente.
- `Genetico/`: Carpeta donde se almacenan los resultados y logs de las ejecuciones.
    - `aux_genetico_drones.py`: Contiene funciones auxiliares para el algoritmo genético.
    - `genetico_drones.py`: Contiene la implementación del algoritmo genético.
    - `gestor_ficheros.py`: Contiene funciones para leer y escribir archivos.
    - `main_genetico_drones.py`: Script principal para ejecutar el algoritmo genético.
- `README.md`: Contiene la documentación necesaria para el correcto uso de este proyecto.

Para asegurar el correcto funcionamiento de los scripts, es importante no separarlos de los que se encuentran en la misma carpeta.

## Generación de escenarios

Para generar un escenario, sitúese en la misma carpeta que generador_escenario.py y utilice el siguiente comando:

```bash
python3 generador_escenario.py [ruta_drones] [ruta_sensores] [ruta_seed_escenario] [ruta_parametros_drones] [ruta_parametros_sensores] [ruta_log] [-s, --seed] valor
```

#### Parámetros Obligatorios:
- `[ruta_drones]`: Ruta del archivo donde se guardarán los parámetros de los drones.
- `[ruta_sensores]`: Ruta del archivo donde se guardarán los parámetros de los sensores.
- `[ruta_seed_escenario]`: Ruta del archivo donde se guardará la seed del escenario.
- `[ruta_parametros_drones]`: Ruta del archivo desde donde se leerán los parámetros para la generación de los drones.
- `[ruta_parametros_sensores]`: Ruta del archivo desde donde se leerán los parámetros para la generación de los sensores.
- `[ruta_log]`: Ruta del archivo donde se escribirá el log.

#### Parámetros Opcionales:
- `-s`, `--seed`: Semilla personalizada para la generación del escenario.

#### Parametros de los drones
Se deben especificar los siguientes parámetros en el archivo de los drones, en el siguiente orden, cada uno en una línea diferente y con un separador de igual (`=`) entre el nombre del parámetro y su valor (el nombre del parámetro no es necesario, pero se debe mantener el orden y el separador):

- `Numero de drones`: Número de drones que se generarán.
- `Distancia minima`: Distancia mínima que puede recorrer un dron.
- `Distancia maxima`: Distancia máxima que puede recorrer un dron.
- `Bateria minima`: Batería mínima que puede tener un dron para recargar sensores.
- `Bateria maxima`: Batería máxima que puede tener un dron para recargar sensores.

#### Parametros de los sensores
Se deben especificar los siguientes parámetros en el archivo de los sensores, en el siguiente orden, cada uno en una línea diferente y con un separador de igual (`=`) entre el nombre del parámetro y su valor (el nombre del parámetro no es necesario, pero se debe mantener el orden y el separador):

- `Numero de sensores`: Número de sensores que se generarán.
- `Coordenada maxima X`: Coordenada máxima en el eje X en la cual se puede generar un sensor.
- `Coordenada maxima Y`: Coordenada máxima en el eje Y en la cual se puede generar un sensor.
- `Prioridad maxima`: Prioridad máxima que puede tener un sensor.
- `Bateria faltante maxima`: Batería faltante máxima que puede tener un sensor.

## Ejecución de algoritmos

### Método exacto: CPLEX

Para ejecutar el método de resolución exacto, sitúese en la misma carpeta que cplex_drones.py y utilice el siguiente comando:

```bash
python3 cplex_drones.py [ruta_drones] [ruta_sensores] [ruta_seed_escenario] [ruta_log] [peso_distancia]
```

#### Parámetros Obligatorios:
- `[ruta_drones]`: Ruta del archivo desde donde se leerán los parámetros de los drones.
- `[ruta_sensores]`: Ruta del archivo desde donde se leerán los parámetros de los sensores.
- `[ruta_seed_escenario]`: Ruta del archivo desde donde se leerá la seed del escenario.
- `[ruta_log]`: Ruta del archivo donde se escribirá el log.
- `[peso_distancia]`: Peso de la distancia en el cálculo del fitness.

### Método aproximado: Algoritmo Genético

Para ejecutar el método de resolución aproximado, sitúese en la misma carpeta que main_genetico_drones.py y utilice el siguiente comando:

```bash
python3 main_genetico_drones.py [ruta_drones] [ruta_sensores] [ruta_seed_escenario] [ruta_log] [ruta_parametros] [peso_distancia] [n_ejecuciones] [-rs, --random_seed] [-s, --seed] valor
```

#### Parámetros Obligatorios:
- `[ruta_drones]`: Ruta del archivo desde donde se leerán los parámetros de los drones.
- `[ruta_sensores]`: Ruta del archivo desde donde se leerán los parámetros de los sensores.
- `[ruta_seed_escenario]`: Ruta del archivo desde donde se leerá la seed del escenario.
- `[ruta_log]`: Ruta del archivo donde se escribirá el log.
- `[ruta_parametros]`: Ruta del archivo desde donde se leerán los parámetros del algoritmo genético.
- `[peso_distancia]`: Peso de la distancia en el cálculo del fitness.
- `[n_ejecuciones]`: Número de ejecuciones del algoritmo genético.

#### Parámetros Opcionales:
- `-rs`, `--random_seed`: Establecer una seed aleatoria para el solucionador.
- `-s`, `--seed`: Semilla personalizada para el solucionador.

Si se utiliza la semilla aleatoria, no se debe establecer la semilla personalizada.

#### Parametros del algoritmo genético

Se deben especificar los siguientes parámetros en el archivo de los parámetros, en el siguiente orden, cada uno en una línea diferente y con un separador de igual (`=`) entre el nombre del parámetro y su valor (el nombre del parámetro no es necesario, pero se debe mantener el orden y el separador):

- `Tamaño de la población`: Número de individuos en la población.
- `Porcentaje mejor`: Porcentaje de la población que se considerará para la selección de los mejores individuos.
- `Probabilidad de cruce`: Probabilidad de que dos individuos se crucen.
- `Probabilidad de mutación`: Probabilidad de que un individuo mute.
- `Máximo de generaciones sin mejora`: Número de generaciones sin mejora antes de detener el algoritmo.

## Repetición de experimentos

Para repetir los experimentos incluidos en la memoria, ejecute los archivos `.bat` proporcionados en el proyecto. Por ejemplo:

```bash
experimento1.bat
```

Cada archivo `.bat` contiene los comandos necesarios para ejecutar los experimentos con los parámetros específicos descritos en la memoria.