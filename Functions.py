from scipy.fftpack import fft
import numpy as np
import matplotlib.pyplot as plt
import random
diccionary = ["Agua","Agua con Jabón", "Tubería Vacía Bomba Prendida","Tubería Vacía Bomba Apagada"]

def fourier(array,i,samples,label):
    mean = np.mean(array)
    array = array - mean
    L = len(array)
    gk = fft(np.array(array))
    M_gk = abs(gk)
    M_gk = M_gk[0:L // 2]
    Fs = samples / 2
    F = (Fs * np.arange(0, L // 2) / L)
    F = F.astype(int)

    return M_gk

def vectorizar(sequences, dim=4):
    restults = np.zeros((len(sequences),dim))
    for i, sequences in enumerate(sequences):
        restults[i,int(sequences)]=1
    return restults


def getFrecuency(df,samples,label,size_fft):
    size = len(df)
    matrix = np.empty((size,size_fft + 1))
    for i in range(0, size):
        #label = df.iloc[i, -1]
        F = fourier(df.iloc[i, :], i, samples,label)
        F = np.append(np.array(F), label)
        matrix[i] = F
    return matrix