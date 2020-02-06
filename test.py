from lib import binToNum, bintransfo, filtre, huffman, msg, signalMod, wavWrite, openOutput, demodBin

message = msg('C:\\Users\\ploui\\Documents\\A1\\Bloc4\\GitHub\\FSK-Modulation\\message.txt')
asciiBin = bintransfo(message)
huff = huffman(message)
print(f'message huffman : {huff}')
#sinNum = binToNum(huff)
sinMod = signalMod(huff)
FFTi = filtre(sinMod, huff)
wavWrite(FFTi,'output.wav')

wavfile = openOutput('output.wav')
print(f'signal démodulé : {demodBin(wavfile)}')
