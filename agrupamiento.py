import pandas as pd
from scipy.stats import wilcoxon
import os
import matplotlib.pyplot as plt

tamanio_conjunto = 2
hasta = 1400
tamanio_muestra = 11
directorios = ['prueba2/db','prueba2/db2','prueba2/db3']

def leer_primeros_datos(ruta):
    df = pd.read_csv(ruta)
    return df['Prueba'].head(tamanio_muestra)


# Función para realizar la prueba de Wilcoxon entre dos grupos de datos
def realizar_prueba_wilcoxon(grupo_base, grupo_comparar):
    stat, p = wilcoxon(grupo_base, grupo_comparar)
    return p, p < 0.05


# Preparar DataFrame para almacenar los resultados
resultados = pd.DataFrame(columns=['Grupo Comparado', 'P-Value', 'Diferencia Significativa'])




# Leer y agrupar los datos del conjunto base (2048, 2047, 2046)
grupo_base = []
grupo_base_promedio = []
for conjunto in range(2048, 2048 - tamanio_conjunto, - 1):
    for directorio in directorios:
        ruta_archivo = f'{directorio}/{conjunto}/Datos.csv'
        if os.path.exists(ruta_archivo):
            grupo_base.extend(leer_primeros_datos(ruta_archivo))

# Asegurar que el grupo base tenga datos antes de proceder
if len(grupo_base) == 0:
    raise ValueError("El grupo base no tiene suficientes datos para realizar la comparación.")

# Comparar el grupo base con los grupos de años subsiguientes
for conjunto_inicio in range(2048- tamanio_conjunto, hasta, - tamanio_conjunto):  # Comenzar desde 2045 y moverse hacia atrás en grupos de 3
    grupo_comparar = []
    for año in range(conjunto_inicio, conjunto_inicio - tamanio_conjunto, - 1):
        for directorio in directorios:
            ruta_archivo = f'{directorio}/{año}/Datos.csv'
            if os.path.exists(ruta_archivo):
                grupo_comparar.extend(leer_primeros_datos(ruta_archivo))

    if len(grupo_comparar) > 0:
        p_value, diff_significativa = realizar_prueba_wilcoxon(grupo_base, grupo_comparar)
        resultados = resultados.append({'Grupo Comparado': f'{conjunto_inicio} a {conjunto_inicio - 1}',
                                        'P-Value': p_value,
                                        'Diferencia Significativa': diff_significativa},
                                       ignore_index=True)



# Convertir la columna 'Diferencia Significativa' a valores numéricos para el gráfico
resultados['Diferencia Numérica'] = resultados['Diferencia Significativa'].astype(int)


plt.figure(figsize=(12, 6))

# Asignar colores en base a la diferencia significativa
colors = ['orange' if significativa else 'blue' for significativa in resultados['Diferencia Significativa']]

plt.scatter(resultados.index, resultados['Diferencia Significativa'].astype(int), color=colors, s=100)

plt.title('Diferencia Significativa por Grupo Comparado Tamaño Grupo (' + str(tamanio_conjunto) + ')')
plt.xlabel('Grupo Comparado')
plt.ylabel('Diferencia Significativa')

# Ajustar las marcas y etiquetas del eje Y para mostrar solo 0 y 1
plt.yticks([0, 1], ['No', 'Sí'])

# Ajustar los ticks del eje x para mostrar solo algunas referencias, evitando saturación
etiquetas_indices = range(0, len(resultados['Grupo Comparado']), 20)
etiquetas = [resultados['Grupo Comparado'][i] if i in etiquetas_indices else '' for i in range(len(resultados['Grupo Comparado']))]
plt.xticks(ticks=range(len(resultados['Grupo Comparado'])), labels=etiquetas, rotation=45, ha='right')

plt.grid(False)
plt.tight_layout()
plt.show()