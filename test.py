from lib import binToNum, bintransfo, filtre, huffman, msg, signalMod, wavWrite

message = msg('message.txt')
asciiBin = bintransfo(message)
huff = huffman(message)
#sinNum = binToNum(asciiBin)
sinMod = signalMod(asciiBin)
FFTi = filtre(sinMod, asciiBin)
wavWrite(FFTi)
