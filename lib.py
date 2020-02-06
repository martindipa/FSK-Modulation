from heapq import heappush, heappop, heapify
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile


def msg(directory):
    msg = open(directory, 'r')
    txt = msg.read()
    msg.close()
    return txt


def bintransfo(msgAscii):                   #Création d'une fonction bintransfo avec une variable msgAscii
    msgBin = []                             #Création d'une liste vide msgBin
    for i in range(0, len(msgAscii)):       #Initialisation d'une boucle pour
        temp = format(ord(msgAscii[i]), '#010b')[2:]#Transformation de notre liste en binaire, de plus on enlève le préfixe
        for i in range(0, len(temp)):       #Initialisation d'une autre boucle pour
            msgBin.append(int(temp[i]))     #On intègre chaque bit à la liste msgBin de façon isolée
    return msgBin  # On renvoie msgBin


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
        #print("%s\t%s\t%s" % (p[0], symb2freq[p[0]], p[1]))
        chaine[p[0]] = p[1]

    result = ""
    for a in txt:
        result += chaine[a]
    return result

def binToNum(codeBin):
    fe=44100                       #fréquence d'échantillonnage
    debit=20
    t = np.arange(0, len(codeBin)/debit, 1/fe)
    list=[]
    a=codeBin
    fb = int(((len(codeBin)/debit)*fe)/len(codeBin))
    for i in range(0, len(a)):
        temp = str(a[i]) * fb
        for j in range(0, len(temp)):
            list.append(int(temp[j]))

    plt.plot(t,list)                     #Affichage via la fonction plot de Matplotlib
    plt.xlabel('Temps (s)')          #définition de l'axe des abscisses
    plt.ylabel('Amplitude')          #définition de l'axe des ordonnées
    plt.title ('Signal S=S1+S2',fontsize=14)
    plt.grid()
    plt.show()                          #affichage d


def signalMod(montxt):
    ##Création signal 1
    ##Signal que l'on va envoyer
    f1 = 19000  # fréquence du signal
    fe = 44100  # fréquence d'échantillonnag
    debit = 20
    t = np.arange(0, len(montxt)/debit, 1/fe)  # creation de la base temps avec numpy
    s1 = np.sin(2*np.pi*f1*t)  # creation d'une sinusoide de Fréquence F


    ##Création signal 2
    ##Signal modulant
    f2 = 21500  # fréquence du signal
    debit = 20
    s2 = np.sin(2*np.pi*f2*t)  # creation d'une sinusoide de Fréquence F


    ##Def de variables
    b = montxt
    b1 = [] #Init de tableau vide
    s = []
    fb = int(((len(montxt)/debit)*fe)/len(montxt))  # Nombre d'échantillon par bit

    ##Duplication d'echantillons par bits
    for i in range(0, len(b)):
        temp = str(b[i]) * fb
        for i in range(0, len(temp)):
            b1.append(int(temp[i]))


    ##Selection entre 2 signaux pour moduler
    for i in range(0, len(b1)):
        if b1[i] == 0:
            s.append(s1[i])
        else:
            s.append(s2[i])

    f3 = 200  # fréquence du signal
    s4 = np.sin(2*np.pi*f3*t)  # creation d'une sinusoide de Fréquence F
    S = s4 + s #Création d'un signal modulé avec bruit

    ##Affichage
    plt.plot(t, S)  # Affichage via la fonction plot de Matplotlib
    plt.title('Signal émis modulé')
    plt.xlabel('Temps (s)')  # définition de l'axe des abscisses
    plt.ylabel('Amplitude')  # définition de l'axe des ordonnées
    plt.grid()
    plt.show()

    return S


def filtre(Signal, montxt):

    #Init variables
    S = Signal
    debit = 20
    fe = 44100
    fc = 18000
    t = np.arange(0, len(montxt)/debit, 1/fe)

    #Filtre
    FFT = np.fft.fft(S)
    f = np.fft.fftfreq(len(montxt), 1/fe)
    for i in range(len(f)):
        if f[i] < fc:  # on coupe toutes les fréquences < 18000 Hz
            FFT[i] = 0.0

    #FFT Inverse
    FFTi = np.fft.ifft(FFT)

    #Affichage
    plt.plot(t, FFTi)  # Affichage via la fonction plot de Matplotlib
    plt.xlabel('Temps (s)')  # définition de l'axe des abscisses
    plt.ylabel('Module')  # définition de l'axe des ordonnées
    plt.xlim(0)
    plt.grid()
    plt.title('signal filtré S(t)', fontsize=14)
    plt.show()

    return FFTi

def wavWrite(data, filename):
    rate = 44100
    wavfile.write(filename, rate, np.float64(data))