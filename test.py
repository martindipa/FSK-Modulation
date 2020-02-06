from lib import bintransfo, msg, huffman, signalMod, binToNum, filtre
import demodulation

message = msg('message.txt')
asciiBin = bintransfo(message)
huff = huffman(message)
#sinNum = binToNum(asciiBin)
sinMod = signalMod(asciiBin)
filtre(sinMod, asciiBin)
#waveMaker(sinMod, 'sinMod.wav')