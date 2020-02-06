import scipy.signal.signaltools as sigtool
from scipy import signal
from scipy.signal import butter, lfilter, blackman
import wave
import struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import rfft, rfftfreq

mark_f = 1200
space_f = 2200
Fs = 44100

waveFile = wave.open("Sample4_160224_mono.wav", "r")
length = waveFile.getnframes()
sig = []
for i in range(0, length):
    waveData = waveFile.readframes(1)
    data = struct.unpack("<h", waveData)
    sig.append(data)


# Bandpass filter mark and space frequencies:

low_bpass = signal.remez(5, [.1,.109,.11,.13,.131,.14],[0,1,0])
mark_filtered = signal.lfilter(low_bpass, 1, sig)

high_bpass = signal.remez(5, [.2,.209,.2100,.23,.231,.2400],[0,1,0])
space_filtered = signal.lfilter(high_bpass, 1, sig)


# Envelope detector on mark and space bandpass filtered signals:

mark_env = np.abs(sigtool.hilbert(mark_filtered))
space_env = np.abs(sigtool.hilbert(space_filtered))


# Compare and decision:

seq = range(0, len(mark_env))
rx = []
for i in seq:
    if mark_env[i] > space_env[i]:
        rx.append(1)
    if mark_env[i] < space_env[i]:
        rx.append(0)
    if mark_env[i] == space_env[i]:
        rx.append(0)