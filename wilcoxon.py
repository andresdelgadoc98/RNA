import os
import pandas as pd
from scipy.stats import wilcoxon
import numpy as np
import matplotlib.pyplot as plt

# Definir los directorios base y las carpetas a analizar
base_directories = ['prueba2/db','prueba2/db2', 'prueba2/db3']
folder_range = range(2014, 1400,-1,)  # Incluye el 2048 y va hacia atrás hasta el 1400
reference_folder = 2014
num_samples = 11

# Preparar un diccionario para almacenar los datos de referencia (carpeta 2048) de cada base
reference_data = {db: None for db in base_directories}

# Preparar un diccionario para almacenar los resultados
wilcoxon_results = []

# Leer y almacenar los datos de la carpeta de referencia 2048 de cada base
for db in base_directories:
    path = os.path.join(db, str(reference_folder), "datos.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
        # Asegurarse de que hay suficientes datos y tomar los primeros 11
        if len(df) >= num_samples:
            reference_data[db] = df["Prueba"].head(num_samples)
            lista_de_prueba = reference_data[db].tolist()

# Ahora revisar las otras carpetas y realizar el test de Wilcoxon contra la referencia
for folder in folder_range: 
    if folder == reference_folder:
        continue  # Saltar la carpeta de referencia

    # Almacenar los datos de cada base para esta carpeta
    folder_data = []

    for db in base_directories:
        path = os.path.join(db, str(folder), "datos.csv")
        if os.path.exists(path):
            df = pd.read_csv(path)
            # Asegurarse de que hay suficientes datos y tomar los primeros 11
            if len(df) >= num_samples:
                folder_data.append(df["Prueba"].head(num_samples))

    # Combinar los datos de las tres bases si todos están disponibles
    if len(folder_data) == 3:
        combined_data = pd.concat(folder_data)
        combined_reference_data = pd.concat([reference_data[db] for db in base_directories if reference_data[db] is not None])

        # Realizar el test de Wilcoxon
        if len(combined_data) == len(combined_reference_data):  # Asegurar que ambos conjuntos tienen el mismo tamaño
            stat, p_value = wilcoxon(combined_reference_data, combined_data)
            significant = "Yes" if p_value < 0.05 else "No"

            wilcoxon_results.append({'Folder': folder, 'P-Value': p_value, 'Significant': significant})

    stat, p_value = wilcoxon(lista_de_prueba, folder_data[0])
    significant = "Yes" if p_value < 0.05 else "No"
    wilcoxon_results.append({'Folder': folder, 'P-Value': p_value, 'Significant': significant})

# Convertir los resultados en un DataFrame y guardarlos en un CSV
results_df = pd.DataFrame(wilcoxon_results)
results_path = "wilcoxon_comparison_results.csv"
results_df.to_csv(results_path, index=False)

df = pd.DataFrame(results_df)

# Visualizar el DataFrame
print(df)

# Graficar
plt.figure(figsize=(10, 6))
for significant, group in df.groupby('Significant'):
    plt.scatter(group['Folder'], [1 if significant == 'Yes' else 0] * len(group), label=significant, alpha=0.6, s=100)

plt.title('Distribución de Significancia ' + str(reference_folder))
plt.xlabel('Número')
plt.yticks([0, 1], ['No', 'Yes'])
plt.ylabel('Significant')
plt.legend()
plt.grid(True)
plt.show()
