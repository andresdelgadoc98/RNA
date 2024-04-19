import os

# Lista de directorios base a revisar
directorios_base = ['prueba2/dbfull']

# Rango de directorios internos a revisar
rango_directorios = range(2048, 1400, -1) # Hasta 1600, decrementando

# Función para revisar la existencia de 'datos.csv' en un directorio
def revisar_datos_csv(directorio):
    for db in directorios_base:
        path_db = os.path.join(directorio, db) # Construye el path completo
        ultimo_con_archivo = None
        for num in rango_directorios:
            path_completo = os.path.join(path_db, str(num), 'datos.csv')
            if os.path.isfile(path_completo):
                ultimo_con_archivo = num
            else:
                break
        if ultimo_con_archivo:
            print(f"En '{db}', el último directorio con 'datos.csv' es: {ultimo_con_archivo}")
        else:
            print(f"No se encontró 'datos.csv' en ninguno de los directorios de '{db}'.")

# Ejecuta la función para la revisión, asumiendo que este script se ejecuta en el directorio que contiene a 'db', 'db2', 'db3'
revisar_datos_csv('.')
