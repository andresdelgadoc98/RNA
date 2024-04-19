import pandas as pd
from sklearn.utils import shuffle
from Functions import vectorizar,getFrecuency
import numpy as np

dbs = ["db2","db","db3"]
raiz = "prueba2/"

#vector = list(range(2048, 1601, -1))
vector = [2046]
for db in dbs:
    print(db)
    for samples in vector:
        print(samples)
        size_fft = int(samples / 2)
        #db2 hacer otra vez con 2048
        df1 = pd.read_csv(db +'/water.csv').iloc[:1000, 1:samples + 1]
        df2 = pd.read_csv(db +'/soap.csv').iloc[:1000, 1:samples + 1]
        df3 = pd.read_csv(db +'/empty-bomb-on.csv').iloc[:1000, 1:samples + 1]
        df4 = pd.read_csv(db +'/empty-bomb-off.csv').iloc[:1000, 1:samples + 1]

        matrix = getFrecuency(df1,samples,0,size_fft)
        matrix = np.vstack((matrix,getFrecuency(df2,samples,1,size_fft)))
        matrix = np.vstack((matrix,getFrecuency(df3,samples,2,size_fft)))
        matrix = np.vstack((matrix,getFrecuency(df4,samples,3,size_fft)))
        df = pd.DataFrame(matrix)

        #df = pd.read_csv('db/' + str(samples) + '/data_curated.csv')

        # Suponiendo que tienes una columna llamada 'clase' que indica la clase de cada ejemplo
        classes = [0,1,2,3]

        train_dfs = []
        validation_dfs = []
        test_dfs = []

        for c in classes:
            df_class = df[df[size_fft] == c]

            # Mezclar los datos por si no están aleatorios
            df_class = shuffle(df_class, random_state=42).reset_index(drop=True)

            train_class = df_class.iloc[:500]
            validation_class = df_class.iloc[500:750]
            test_class = df_class.iloc[750:1000]

            train_dfs.append(train_class)
            validation_dfs.append(validation_class)
            test_dfs.append(test_class)

        train = pd.concat(train_dfs).reset_index(drop=True)
        validation = pd.concat(validation_dfs).reset_index(drop=True)
        test = pd.concat(test_dfs).reset_index(drop=True)

        # Mezcla nuevamente para no tener todos los ejemplos de una clase agrupados
        train = shuffle(train, random_state=42).reset_index(drop=True)
        validation = shuffle(validation, random_state=42).reset_index(drop=True)
        test = shuffle(test, random_state=42).reset_index(drop=True)

        # Guarda en archivos CSV
        train.to_csv(raiz + db + '/' + str(samples) + '/train.csv', index=False)
        validation.to_csv(raiz + db + '/' + str(samples) + '/validation.csv', index=False)
        test.to_csv(raiz + db + '/' + str(samples) + '/test.csv', index=False)