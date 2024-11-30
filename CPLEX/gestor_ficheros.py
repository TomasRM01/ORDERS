from pathlib import Path

# Funcion que recibe la ruta de un fichero y el modo de apertura y devuelve el fichero abierto
def abrirFichero(ruta, modo):
    
    ruta_path = Path(ruta)
    
    # Verificar si la ruta es absoluta o relativa
    if not ruta_path.is_absolute():
        # Convertir la ruta relativa a una ruta absoluta desde el directorio de trabajo actual
        current_working_directory = Path.cwd()  # Directorio de trabajo actual
        ruta_absoluta = (current_working_directory / ruta).resolve()
    else:
        ruta_absoluta = ruta_path.resolve()
    
    ruta_absoluta = Path(ruta_absoluta).resolve()
    
    # Si no existe el directorio
    if not ruta_absoluta.parent.exists():
        if 'w' in modo or 'a' in modo:  # Crear directorios si es modo escritura
            ruta_absoluta.parent.mkdir(parents=True, exist_ok=True)
        else:
            raise FileNotFoundError(f"La ruta {ruta_absoluta.parent} no existe.")
    
    # Si no existe el fichero
    if not ruta_absoluta.exists():
        if 'r' in modo:  # Si es modo lectura, lanzar excepción
            raise FileNotFoundError(f"El fichero {ruta_absoluta} no existe.")
        else:  # Si es modo escritura, crear fichero
            ruta_absoluta.touch()
    
    return ruta_absoluta.open(modo)