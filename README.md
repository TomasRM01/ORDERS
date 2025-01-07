# Optimización de Rutas para Drones En Redes de Sensores (ORDERS)
## Instrucciones para clonar el repositorio

Para clonar el repositorio, ejecute el siguiente comando en su terminal:

```bash
git clone https://github.com/TomasRM01/ORDERS.git
```

## Instalación de dependencias

Se requiere el uso de la versión 3.10 de Python. Puedes descargarla en el siguiente enlace: [Python 3.10.11](https://www.python.org/downloads/release/python-31011/). 

> [!NOTE]  
> Para el desarrollo y testeo de este proyecto, se utilizó la versión 3.10.11 de Python.

Navegue al directorio del proyecto y ejecute el siguiente comando para instalar las dependencias necesarias:

```bash
pip install matplotlib PyQt6
```

Para usar el resolutor de CPLEX, es necesario tener instalado IBM ILOG CPLEX Optimization Studio. Puede descargar una versión completa académica en el siguiente enlace: [IBM ILOG CPLEX Optimization Studio](https://academic.ibm.com/a2mt/downloads/data_science#/).

> [!NOTE]  
> Debes registrarte con tu correo institucional para poder descargar la versión completa.

Una vez instalado, para configurar CPLEX con Python, navegue a la carpeta de instalación de CPLEX y ejecute el siguiente comando como administrador:

```bash
cd IBM\ILOG\CPLEX_Studio2211\python
python3 setup.py install
```

Para terminar, instalamos docplex. Este no soporta numpy 2.0.1, por lo que se debe instalar una version anterior:

```bash
pip install docplex "numpy<2.0"
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
│   ├── cplex_escenario_grande.bat
│   ├── cplex_escenario_mediano.bat
│   ├── cplex_escenario_mini.bat
│   ├── gestor_ficheros.py
│   └── main_cplex.py
├── Escenarios/
│   ├── Grande/
│   │   ├── Parametros_Generador/
│   │   │   ├── params_escenario_grande_drones.txt
│   │   │   ├── params_escenario_grande_seed.txt
│   │   │   └── params_escenario_grande_sensores.txt
│   │   ├── Parametros_Solucionador/
│   │   │   ├── escenario_grande_drones.txt
│   │   │   ├── escenario_grande_sensores.txt
│   │   │   └── params_genetico_escenario_grande.txt
│   │   └── escenario_grande_sensores.png
│   ├── Mediano/
│   │   ├── Parametros_Generador/
│   │   │   ├── params_escenario_mediano_drones.txt
│   │   │   ├── params_escenario_mediano_seed.txt
│   │   │   └── params_escenario_mediano_sensores.txt
│   │   ├── Parametros_Solucionador/
│   │   │   ├── escenario_mediano_drones.txt
│   │   │   ├── escenario_mediano_sensores.txt
│   │   │   └── params_genetico_escenario_mediano.txt
│   │   └── escenario_mediano_sensores.png
│   └── Mini/
│       ├── Parametros_Generador/
│       │   ├── params_escenario_mini_drones.txt
│       │   ├── params_escenario_mini_seed.txt
│       │   └── params_escenario_mini_sensores.txt
│       ├── Parametros_Solucionador/
│       │   ├── escenario_mini_drones.txt
│       │   ├── escenario_mini_sensores.txt
│       │   └── params_genetico_escenario_mini.txt
│       └── escenario_mini_sensores.png
├── Generador/
│   ├── generador_drones.py
│   ├── generador_escenario_grande.bat
│   ├── generador_escenario_mediano.bat
│   ├── generador_escenario_mini.bat
│   ├── generador_escenario.py
│   ├── generador_sensores.py
│   ├── gestor_ficheros.py
│   ├── imprime_sensores_grande.bat
│   ├── imprime_sensores_mediano.bat
│   ├── imprime_sensores_mini.bat
│   ├── imprime_sensores.py
│   └── log_generador_escenario.txt
├── Genetico/
│   ├── aux_genetico.py
│   ├── genetico_escenario_grande.bat
│   ├── genetico_escenario_mediano.bat
│   ├── genetico_escenario_mini.bat
│   ├── genetico.py
│   ├── gestor_ficheros.py
│   └── main_genetico.py
├── Resultados/
│   ├── Grande/
│   │   ├── caminos_genetico_escenario_grande.png
│   │   ├── diagrama_genetico_escenario_grande.png
│   │   ├── log_cplex_escenario_grande.txt
│   │   └── log_genetico_escenario_grande.txt
│   ├── Mediano/
│   │   ├── caminos_cplex_escenario_mediano.png
│   │   ├── caminos_genetico_escenario_mediano.png
│   │   ├── diagrama_genetico_escenario_mediano.png
│   │   ├── log_cplex_escenario_mediano.txt
│   │   └── log_genetico_escenario_mediano.txt
│   └── Mini/
│       ├── caminos_cplex_escenario_mini.png
│       ├── caminos_genetico_escenario_mini.png
│       ├── diagrama_genetico_escenario_mini.png
│       ├── log_cplex_escenario_mini.txt
│       └── log_genetico_escenario_mini.txt
├── .gitignore
└── README.md
```

- `CPLEX/`: Contiene los scripts necesarios para utilizar el método de resolución exacto.
    - `cplex_escenario_grande.bat`: Script para ejecutar el método exacto en el escenario grande.
    - `cplex_escenario_mediano.bat`: Script para ejecutar el método exacto en el escenario mediano.
    - `cplex_escenario_mini.bat`: Script para ejecutar el método exacto en el escenario mini.
    - `gestor_ficheros.py`: Contiene funciones para leer y escribir archivos.
    - `main_cplex.py`: Script principal para ejecutar el método de resolución exacto.
- `Escenarios/`: Contiene los parámetros de los drones, sensores y semilla.
    - `Grande/`: Carpeta con los parámetros del escenario grande.
        - `Parametros_Generador/`: Parámetros para la generación del escenario grande.
            - `params_escenario_grande_drones.txt`: Parámetros de los drones utilizados para generar el escenario grande.
            - `params_escenario_grande_seed.txt`: Seed utilizada para generar el escenario grande.
            - `params_escenario_grande_sensores.txt`: Parámetros de los sensores utilizados para generar el escenario grande.
        - `Parametros_Solucionador/`: Parámetros del escenario grande para los solucionadores.
            - `escenario_grande_drones.txt`: Parámetros de los drones utilizados para resolver el escenario grande.
            - `escenario_grande_sensores.txt`: Parámetros de los sensores utilizados para resolver el escenario grande.
            - `params_genetico_escenario_grande.txt`: Parámetros del algoritmo genético para el escenario grande.
        - `escenario_grande_sensores.png`: Imagen de los sensores en el escenario grande.
    - `Mediano/`: Carpeta con los parámetros del escenario mediano.
        - `Parametros_Generador/`: Parámetros para la generación del escenario mediano.
            - `params_escenario_mediano_drones.txt`: Parámetros de los drones utilizados para generar el escenario mediano.
            - `params_escenario_mediano_seed.txt`: Seed utilizada para generar el escenario mediano.
            - `params_escenario_mediano_sensores.txt`: Parámetros de los sensores utilizados para generar el escenario mediano.
        - `Parametros_Solucionador/`: Parámetros del escenario mediano para los solucionadores.
            - `escenario_mediano_drones.txt`: Parámetros de los drones utilizados para resolver el escenario mediano.
            - `escenario_mediano_sensores.txt`: Parámetros de los sensores utilizados para resolver el escenario mediano.
            - `params_genetico_escenario_mediano.txt`: Parámetros del algoritmo genético para el escenario mediano.
        - `escenario_mediano_sensores.png`: Imagen de los sensores en el escenario mediano.
    - `Mini/`: Carpeta con los parámetros del escenario mini.
        - `Parametros_Generador/`: Parámetros para la generación del escenario mini.
            - `params_escenario_mini_drones.txt`: Parámetros de los drones utilizados para generar el escenario mini.
            - `params_escenario_mini_seed.txt`: Seed utilizada para generar el escenario mini.
            - `params_escenario_mini_sensores.txt`: Parámetros de los sensores utilizados para generar el escenario mini.
        - `Parametros_Solucionador/`: Parámetros del escenario mini para los solucionadores.
            - `escenario_mini_drones.txt`: Parámetros de los drones utilizados para resolver el escenario mini.
            - `escenario_mini_sensores.txt`: Parámetros de los sensores utilizados para resolver el escenario mini.
            - `params_genetico_escenario_mini.txt`: Parámetros del algoritmo genético para el escenario mini.
        - `escenario_mini_sensores.png`: Imagen de los sensores en el escenario mini.
- `Generador/`: Contiene los scripts necesarios para generar escenarios.
    - `generador_drones.py`: Script que contiene el código necesario para generar drones.
    - `generador_escenario_grande.bat`: Script para generar el escenario grande.
    - `generador_escenario_mediano.bat`: Script para generar el escenario mediano.
    - `generador_escenario_mini.bat`: Script para generar el escenario mini.
    - `generador_escenario.py`: Este script genera un escenario con drones y sensores utilizando generador_drones.py y generador_sensores.py.
    - `generador_sensores.py`: Script que contiene el código necesario para generar sensores.
    - `gestor_ficheros.py`: Contiene funciones para leer y escribir archivos.
    - `imprime_sensores_grande.bat`: Script para imprimir los sensores del escenario grande.
    - `imprime_sensores_mediano.bat`: Script para imprimir los sensores del escenario mediano.
    - `imprime_sensores_mini.bat`: Script para imprimir los sensores del escenario mini.
    - `imprime_sensores.py`: Script que imprime los sensores del escenario y los representa gráficamente.
    - `log_generador_escenario.txt`: Log de la generación de los escenarios.
- `Genetico/`: Carpeta donde se almacenan los resultados y logs de las ejecuciones.
    - `aux_genetico.py`: Contiene funciones auxiliares para el algoritmo genético.
    - `genetico_escenario_grande.bat`: Script para ejecutar el algoritmo genético en el escenario grande.
    - `genetico_escenario_mediano.bat`: Script para ejecutar el algoritmo genético en el escenario mediano.
    - `genetico_escenario_mini.bat`: Script para ejecutar el algoritmo genético en el escenario mini.
    - `genetico.py`: Contiene la implementación del algoritmo genético.
    - `gestor_ficheros.py`: Contiene funciones para leer y escribir archivos.
    - `main_genetico.py`: Script principal para ejecutar el algoritmo genético.
- `Resultados/`: Contiene los resultados de los experimentos
    - `Grande/`: Carpeta con los resultados del escenario grande.
        - `caminos_genetico_escenario_grande.png`: Gráfica de los caminos obtenidos por el algoritmo genético en el escenario grande.
        - `diagrama_genetico_escenario_grande.png`: Diagrama de caja y bigotes de las ejecuciones del algoritmo genético para el escenario grande.
        - `log_cplex_escenario_grande.txt`: Log de la ejecución del método exacto en el escenario grande.
        - `log_genetico_escenario_grande.txt`: Log de la ejecución del algoritmo genético en el escenario grande.
    - `Mediano/`: Carpeta con los resultados del escenario mediano.
        - `caminos_genetico_escenario_mediano.png`: Gráfica de los caminos obtenidos por el algoritmo genético en el escenario mediano.
        - `caminos_cplex_escenario_mediano.png`: Gráfica de los caminos obtenidos por el método exacto en el escenario mediano.
        - `diagrama_genetico_escenario_mediano.png`: Diagrama de caja y bigotes de las ejecuciones del algoritmo genético para el escenario mediano.
        - `log_genetico_escenario_mediano.txt`: Log de la ejecución del algoritmo genético en el escenario mediano.
        - `log_cplex_escenario_mediano.txt`: Log de la ejecución del método exacto en el escenario mediano.
    - `Mini/`: Carpeta con los resultados del escenario mini.
        - `caminos_genetico_escenario_mini.png`: Gráfica de los caminos obtenidos por el algoritmo genético en el escenario mini.
        - `caminos_cplex_escenario_mini.png`: Gráfica de los caminos obtenidos por el método exacto en el escenario mini.
        - `diagrama_genetico_escenario_mini.png`: Diagrama de caja y bigotes de las ejecuciones del algoritmo genético para el escenario mini.
        - `log_genetico_escenario_mini.txt`: Log de la ejecución del algoritmo genético en el escenario mini.
        - `log_cplex_escenario_mini.txt`: Log de la ejecución del método exacto en el escenario mini.
- `.gitignore`: Archivo que contiene los archivos y carpetas que se ignoran en el control de versiones.
- `README.md`: Contiene la documentación necesaria para el correcto uso de este proyecto.

> [!CAUTION]
> Para asegurar el correcto funcionamiento de los scripts, es importante no separarlos de los que se encuentran en la misma carpeta.

## Generación de escenarios

Para generar un escenario, sitúese en la misma carpeta que generador_escenario.py y utilice el siguiente comando:

```bash
python3 generador_escenario.py [ruta_drones] [ruta_sensores] [ruta_seed_escenario] [ruta_parametros_drones] [ruta_parametros_sensores] [ruta_log] [-s, --seed] valor
```

#### Parámetros Obligatorios
- `ruta_drones`: Ruta del archivo donde se guardarán los parámetros de los drones.
- `ruta_sensores`: Ruta del archivo donde se guardarán los parámetros de los sensores.
- `ruta_seed_escenario`: Ruta del archivo donde se guardará la seed del escenario.
- `ruta_parametros_drones`: Ruta del archivo desde donde se leerán los parámetros para la generación de los drones.
- `ruta_parametros_sensores`: Ruta del archivo desde donde se leerán los parámetros para la generación de los sensores.
- `ruta_log`: Ruta del archivo donde se escribirá el log.

#### Parámetros Opcionales
- `-s`, `--seed`: Semilla personalizada para la generación del escenario.

#### Parametros de los drones
Se deben especificar los siguientes parámetros en el archivo de los drones, en el siguiente orden, cada uno en una línea diferente y con un separador de igual (`=`) entre el nombre del parámetro y su valor:

- `Numero de drones`: Número de drones que se generarán.
- `Distancia minima`: Distancia mínima que puede recorrer un dron.
- `Distancia maxima`: Distancia máxima que puede recorrer un dron.
- `Bateria minima`: Batería mínima que puede tener un dron para recargar sensores.
- `Bateria maxima`: Batería máxima que puede tener un dron para recargar sensores.

> [!IMPORTANT]  
> El nombre del parámetro no es necesario, pero se debe mantener el orden y el separador.

#### Parametros de los sensores
Se deben especificar los siguientes parámetros en el archivo de los sensores, en el siguiente orden, cada uno en una línea diferente y con un separador de igual (`=`) entre el nombre del parámetro y su valor:

- `Numero de sensores`: Número de sensores que se generarán.
- `Coordenada maxima X`: Coordenada máxima en el eje X en la cual se puede generar un sensor.
- `Coordenada maxima Y`: Coordenada máxima en el eje Y en la cual se puede generar un sensor.
- `Prioridad maxima`: Prioridad máxima que puede tener un sensor.
- `Bateria faltante maxima`: Batería faltante máxima que puede tener un sensor.

> [!IMPORTANT]  
> El nombre del parámetro no es necesario, pero se debe mantener el orden y el separador.

## Ejecución de algoritmos

### Método exacto: CPLEX

Para ejecutar el método de resolución exacto, sitúese en la misma carpeta que `main_cplex.py` y utilice el siguiente comando:

```bash
python3 main_cplex.py [ruta_drones] [ruta_sensores] [ruta_seed_escenario] [ruta_log] [peso_distancia] [-v, --verbalize] [-g, --mipgap] valor
```

#### Parámetros Obligatorios
- `ruta_drones`: Ruta del archivo desde donde se leerán los parámetros de los drones.
- `ruta_sensores`: Ruta del archivo desde donde se leerán los parámetros de los sensores.
- `ruta_seed_escenario`: Ruta del archivo desde donde se leerá la seed del escenario.
- `ruta_log`: Ruta del archivo donde se escribirá el log.
- `peso_distancia`: Peso de la distancia en el cálculo del fitness.

#### Parámetros Opcionales
- `-v`, `--verbalize`: Imprimir información adicional durante la ejecución.
- `-g`, `--mipgap`: Establecer el valor de la tolerancia de la brecha de la solución. Por defecto es *0.0001*.

> [!CAUTION]
> Cuanto más grande sea el `--mipgap`, menor será la precisión del resultado.

### Método aproximado: Algoritmo Genético

Para ejecutar el método de resolución aproximado, sitúese en la misma carpeta que `main_genetico.py` y utilice el siguiente comando:

```bash
python3 main_genetico.py [ruta_drones] [ruta_sensores] [ruta_seed_escenario] [ruta_log] [ruta_parametros] [peso_distancia] [n_ejecuciones] [-rs, --random_seed] [-s, --seed] valor
```

#### Parámetros Obligatorios
- `ruta_drones`: Ruta del archivo desde donde se leerán los parámetros de los drones.
- `ruta_sensores`: Ruta del archivo desde donde se leerán los parámetros de los sensores.
- `ruta_seed_escenario`: Ruta del archivo desde donde se leerá la seed del escenario.
- `ruta_log`: Ruta del archivo donde se escribirá el log.
- `ruta_parametros`: Ruta del archivo desde donde se leerán los parámetros del algoritmo genético.
- `peso_distancia`: Peso de la distancia en el cálculo del fitness.
- `n_ejecuciones`: Número de ejecuciones del algoritmo genético.

#### Parámetros Opcionales
- `-rs`, `--random_seed`: Establecer una seed aleatoria para el solucionador.
- `-s`, `--seed`: Semilla personalizada para el solucionador.

> [!CAUTION]
> Si se utiliza la semilla aleatoria, no se debe establecer la semilla personalizada.

#### Parametros del algoritmo genético

Se deben especificar los siguientes parámetros en el archivo de los parámetros, en el siguiente orden, cada uno en una línea diferente y con un separador de igual (`=`) entre el nombre del parámetro y su valor:

- `Tamaño de la población`: Número de individuos en la población.
- `Porcentaje mejor`: Porcentaje de la población que se considerará para la selección de los mejores individuos.
- `Probabilidad de cruce`: Probabilidad de que dos individuos se crucen.
- `Probabilidad de mutación`: Probabilidad de que un individuo mute.
- `Máximo de generaciones sin mejora`: Número de generaciones sin mejora antes de detener el algoritmo.

> [!IMPORTANT]  
> El nombre del parámetro no es necesario, pero se debe mantener el orden y el separador.

## Repetición de experimentos

Para repetir los experimentos incluidos en la memoria, ejecute los archivos `.bat` proporcionados en el proyecto correspondientes a cada escenario.

> [!WARNING]
> Se utilizan rutas relativas en estos archivos, por lo que es importante que no se modifique la estructura del proyecto si se quieren replicar los experimentos.

- Para volver a generar los escenarios de los experimentos, use `generador_escenario_grande.bat`, `generador_escenario_mediano.bat` o `generador_escenario_mini.bat`.

- Para visualizar de forma gráfica los sensores de los escenarios, use `imprime_sensores_grande.bat`, `imprime_sensores_mediano.bat` o `imprime_sensores_mini.bat`.

- Para resolver los escenarios de los experimentos mediante el método exacto, use `cplex_escenario_grande.bat`, `cplex_escenario_mediano.bat` o `cplex_escenario_mini.bat`.

- Para resolver los escenarios de los experimentos mediante el método aproximado, use `genetico_escenario_grande.bat`, `genetico_escenario_mediano.bat` o `genetico_escenario_mini.bat`.

Cada archivo `.bat` contiene los comandos necesarios para ejecutar los experimentos con los parámetros específicos descritos en la memoria.
