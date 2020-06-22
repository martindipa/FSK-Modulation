from heapq import heappush, heappop, heapify
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import periodogram
import soundfile as sf


def msg(directory):
    msg = open(directory, 'r')
    txt = msg.read()
    msg.close()
    return txt


def bintransfo(msgAscii):
    msgBin = []
    for i in range(0, len(msgAscii)):
        temp = format(ord(msgAscii[i]), '#010b')[2:]
        for i in range(0, len(temp)):
            msgBin.append(int(temp[i]))
    return msgBin


def encode(symb2freq):
    heap = [[wt, [sym, ""]] for sym, wt in symb2freq.items()]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))


def huffman(txt):
    chaine = {}
    symb2freq = defaultdict(int)
    for ch in txt:
        symb2freq[ch] += 1
    huff = encode(symb2freq)
    for p in huff:
        chaine[p[0]] = p[1]

    result = ""
    for a in txt:
        result += chaine[a]
    return result


def binToNum(codeBin):
    fe = 44100
    debit = 20
    t = np.arange(0, len(codeBin)/debit, 1/fe)
    list = []
    a = codeBin
    fb = int(((len(codeBin)/debit)*fe)/len(codeBin))
    for i in range(0, len(a)):
        temp = str(a[i]) * fb
        for j in range(0, len(temp)):
            list.append(int(temp[j]))

    plt.plot(t, list)
    plt.xlabel('Temps (s)')
    plt.ylabel('Amplitude')
    plt.title('Signal S=S1+S2', fontsize=14)
    plt.grid()
    plt.show()


def signalMod(montxt):
    f1 = 19000
    fe = 44100
    debit = 20
    t = np.arange(0, len(montxt)/debit, 1/fe)
    s1 = np.sin(2*np.pi*f1*t)
    f2 = 21500
    debit = 20
    s2 = np.sin(2*np.pi*f2*t)
    b = montxt
    f3 = 100
    s4 = np.sin(2*np.pi*f3*t)
    S = s4 + s
    fb = int(((len(montxt)/debit)*fe)/len(montxt))

    b1 = []
    s = []
    for i in range(0, len(b)):
        temp = str(b[i]) * fb
        for i in range(0, len(temp)):
            b1.append(int(temp[i]))

    for i in range(0, len(b1)):
        if b1[i] == 0:
            s.append(s1[i])
        else:
            s.append(s2[i])

    plt.plot(t, S)
    plt.title('Modulated signal')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid()
    plt.show()
    return S


def filtre(Signal, montxt):
    S = Signal
    debit = 20
    fe = 44100
    fc = 18000
    t = np.arange(0, len(montxt)/debit, 1/fe)
    FFT = np.fft.fft(S)
    freq = np.fft.fftfreq(len(S), 1/fe)
    f = freq[:int(len(S)/2)]

    for i in range(len(f)):
        if f[i] < fc:
            FFT[i] = 0.0

    FFTi = np.fft.ifft(FFT)

    plt.plot(t, FFTi)
    plt.xlabel('Time (s)')
    plt.ylabel('Module')
    plt.xlim(0)
    plt.grid()
    plt.title('filtered signal', fontsize=14)
    plt.show()

    return FFTi


def wavWrite(data, filename):
    rate = 44100
    wavfile.write(filename, rate, np.float64(data))


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
        elif r[i] > 20250:
            codebin += '1'

    return codebin
