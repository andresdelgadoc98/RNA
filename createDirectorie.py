import os

# Ruta base donde se crearán los directorios
ruta_base = "prueba2/dbfull"

# Crear directorios con nombres del 1600 al 1400 (en orden descendente)
for i in range(2048, 2047, -1):
    path = os.path.join(ruta_base, str(i))
    os.makedirs(path, exist_ok=True)

# Verificar algunos de los directorios creados
os.listdir(ruta_base)[:10]  # Mostrar solo los primeros 10 directorios creados
