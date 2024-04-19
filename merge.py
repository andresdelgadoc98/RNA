import pandas as pd


dbs = ['db','db2','db3']
samples = list(range(1624, 1600, -1))
files = ['test','train','validation']
raiz = "prueba2/"

for sample in samples:
    print(sample)
    for file in files:
        #df1 = pd.read_csv('db/' + str(sample)  + "/" + str(file) + '.csv').iloc[:1000,1:-1]
        df1 = pd.read_csv(raiz + 'db/' + str(sample)  + "/" + str(file) + '.csv').iloc[:1000,:]
        df2 = pd.read_csv(raiz + 'db2/' + str(sample)  + "/" + str(file) + '.csv').iloc[:1000,:]
        df3 = pd.read_csv(raiz + 'db3/' + str(sample)  + "/" + str(file) + '.csv').iloc[:1000,:]

        df_concatenado = pd.concat([df1, df2, df3])
        ruta_guardado = raiz + 'dbfull/'+ str(sample) + "/" + str(file) +'.csv'
        df_concatenado.to_csv(ruta_guardado, index=False, )