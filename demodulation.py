from scipy.signal import periodogram
import soundfile as sf
import matplotlib.pyplot as plt

r = []
data, Fe = sf.read('output.wav')
p = int(Fe*0.05)
for j in range(int(len(data/p)-1)):
    f, FFT = periodogram(data[j*p:(j+1)*p], Fe)
    for i in range(len(FFT)):
        if FFT[i] > 0.01:
            r.append(f[i])
            break


print(r)
print(len(r))
def demodBin(r):
    codebin = ''
    for i in range(len(r)):
        if r[i] < 20250:
            codebin += '0'
        elif r[i] > 2050:
            codebin += '1'

    return codebin
