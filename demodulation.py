from scipy.signal import periodogram
import soundfile as sf
import matplotlib.pyplot as plt
def openOutput(filename):
    r = []
    debit = 20
    data, Fe = sf.read(filename)
    p = int(Fe*1/debit)
    for j in range(int(len(data/p)-1)):
        f, FFT = periodogram(data[j*p:(j+1)*p], Fe)
        for i in range(len(FFT)):
            if FFT[i] > 0.01:
                r.append(f[i])
                break
    return r

def demodBin(r):
    codebin = ''
    for i in range(len(r)):
        if r[i] < 20250:
            codebin += '0'
        elif r[i] > 2050:
            codebin += '1'
    

    return codebin
