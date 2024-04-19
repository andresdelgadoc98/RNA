import matplotlib.pyplot as plt
import os
import pandas as pd

db_dirs = ['db2','db3','db']
base_dir = 'prueba2'
def calcular_promedio_subcarpetas():
    # Diccionario para almacenar las medias de cada carpeta, donde la clave es el número de la carpeta
    promedios_por_carpeta = {}

    for i in range(2048, 1399, -1):
        medias = []
        # Iterar a través de cada directorio para recoger la media de la carpeta específica
        for db_dir in db_dirs:
            folder_path = os.path.join(base_dir, db_dir, str(i))
            csv_file = os.path.join(folder_path, 'Datos.csv')
            if os.path.exists(csv_file):
                df = pd.read_csv(csv_file)
                media = df['Prueba'][:11].mean()
                medias.append(media)

        # Calcular el promedio de las medias recolectadas para la carpeta actual
        if medias:
            promedio_carpeta = sum(medias) / len(medias)
            promedios_por_carpeta[i] = promedio_carpeta

    return promedios_por_carpeta

promedios_subcarpetas = calcular_promedio_subcarpetas()



carpetas_ordenadas = sorted(promedios_subcarpetas.keys())
promedios_ordenados = [promedios_subcarpetas[carpeta] for carpeta in carpetas_ordenadas]

# Crear la gráfica
plt.figure(figsize=(10, 6))
plt.plot(carpetas_ordenadas, promedios_ordenados, marker='', linestyle='-', color='green')
plt.title('Promedio de Pruebas por conjunto ')
plt.xlabel('Número de Mediciones')
plt.ylabel('Promedio de Prueba')
plt.gca().invert_xaxis()  # Asegurar que el eje X comience por 2048
plt.grid(True)
plt.show()
