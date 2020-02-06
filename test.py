from lib import binToNum, bintransfo, filtre, huffman, msg, signalMod, wavWrite
from demodulation import openOutput, demodBin

#message = msg('message.txt')
#asciiBin = bintransfo(message)
#huff = huffman(message)
#print(huff)
# sinNum = binToNum(huff)
#sinMod = signalMod(huff)
#FFTi = filtre(sinMod, huff)
#wavWrite(FFTi,'output.wav')

wavfile = openOutput('output.wav')
print(wavfile)
print(demodBin(wavfile))