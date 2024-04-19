import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from Functions import vectorizar, getFrecuency
from keras import layers, models, Input

import time

import tensorflow as tf

# db = 'db2'

array_samples = list(range(1400, 199, -1)) 

array_samples = [2045]
dbs = ['prueba2/db3']

for db in dbs:
    print(db)
    for samples in array_samples:
        print(samples)
        # samples = 2048
        prom_accuaray_train = []
        prom_accuaray_validation = []
        prom_accuaray_test = []
        prom_time_trainig = []
        prom_time_test = []

        size_fft = int(samples / 2)

        train = pd.read_csv(str(db) + '/' + str(samples) + '/train.csv')
        validation = pd.read_csv(str(db) + '/' + str(samples) + '/validation.csv')
        test = pd.read_csv(str(db) + '/' + str(samples) + '/test.csv')

        # Separar características y etiquetas para el conjunto de entrenamiento
        X_train = train.drop(columns=[str(size_fft)])
        y_train = vectorizar(train[str(size_fft)])

        # Separar características y etiquetas para el conjunto de validación
        X_val = validation.drop(columns=[str(size_fft)])
        y_val = vectorizar(validation[str(size_fft)])

        # Separar características y etiquetas para el conjunto de prueba
        X_test = test.drop(columns=[str(size_fft)])
        y_test = vectorizar(test[str(size_fft)])

        for i in range(0, 33):
            print("corrida: " + str(i))
            # red neuronal
            size_x = X_train.shape[1]
            model = models.Sequential()
            model.add(layers.Dense(20, activation='relu', input_shape=(size_x,)))
            model.add(layers.Dense(20, activation='relu'))
            model.add(layers.Dense(20, activation='relu'))
            model.add(layers.Dense(20, activation='relu'))
            model.add(layers.Dense(4, activation='softmax'))

            model.compile(optimizer='adam',
                          loss='categorical_crossentropy',
                          metrics=['acc']
                          )
            start_time = time.time()
            history = model.fit(X_train, y_train,
                                batch_size=75, epochs=35, validation_data=(X_val, y_val))
            end_time = time.time()
            trainig_time = end_time - start_time
            start_time_2 = time.time()
            test_loss, test_acc = model.evaluate(X_test, y_test)
            end_time_2 = time.time()
            testing_time = end_time_2 - start_time_2

            # estadísticos
            epocas = range(1, len(history.history['loss']) + 1)
            perdidas = history.history['loss']
            exactitud = history.history['acc']
            precision_entrenamiento = history.history['acc']
            precision_validacion = history.history['val_acc']

            prom_time_trainig.append(trainig_time)
            prom_accuaray_train.append(precision_entrenamiento[34])
            prom_accuaray_validation.append(precision_validacion[34])
            prom_accuaray_test.append(test_acc)
            prom_time_test.append(testing_time)

        df = pd.DataFrame(
            {'Entrenamiento': prom_accuaray_train, 'Validación': prom_accuaray_validation, 'Prueba': prom_accuaray_test,
             'Tiempo Entrenamiento (s)': prom_time_trainig, 'Tiempo prueba (s)': prom_time_test})
        df.to_csv(str(db) + "/" + str(samples) + "/" + "datos.csv", index=False)
        # df.to_csv('dbgainnormal-2048-normal.csv', index=False)

promedio = np.mean(prom_accuaray_train)
print(prom_accuaray_train)

promedio_validacion = np.mean(prom_accuaray_validation)
print(prom_accuaray_validation)

promedio_test = np.mean(prom_accuaray_test)
print(prom_accuaray_test)

print("Accuracy on test set:", test_acc)
