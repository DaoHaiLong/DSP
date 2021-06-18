import os
import numpy as np
import scipy as sp
import scipy.io.wavfile
from abstracmethod import*

class PhaseCoding(Audio):
    def ConvertToByte(self, audio):
        # convert into byte array
        try:
            self.rate, self.audioData = sp.io.wavfile.read(audio)
        except:
            pass
        self.audioData = self.audioData.copy()
        self.rate,self.audioData.shape

    # encode
    def encodeAudio(self, location, text) :
    
        self.ConvertToByte(location)

        text = text.ljust(100, '~')

        # step 1 divide into chunks
        textLength = 8 * len(text)

        blockLength = int(2 * 2 ** np.ceil(np.log2(2 * textLength)))
        blockNumber = int(np.ceil(self.audioData.shape[0] / blockLength))

        # checks shape to change data to 1 axis
        if len(self.audioData.shape) == 1:
            self.audioData.resize(blockNumber * blockLength, refcheck=False)
            self.audioData = self.audioData[np.newaxis]
        else:
            self.audioData.resize((blockNumber * blockLength, self.audioData.shape[1]), refcheck=False)
            self.audioData = self.audioData.T

        blocks = self.audioData[0].reshape((blockNumber, blockLength))

        # Calculate DFT using fft
        blocks = np.fft.fft(blocks)

        # calculate magnitudes
        magnitudes = np.abs(blocks)

        # create phase matrix
        phase = np.angle(blocks)

        # get phase differences
        phaseDiffs = np.diff(phase, axis=0)

        # conert message to encode into binary
        textInBinary = np.ravel([[int(y) for y in format(ord(x), "08b")] for x in text])

        # Convert txt to phase differences
        textInPi = textInBinary.copy()
        textInPi[textInPi == 0] = -1
        textInPi = textInPi * -np.pi / 2

        blockMid = blockLength // 2

        # do phase conversion
        phase[0, blockMid - textLength: blockMid] = textInPi
        phase[0, blockMid + 1: blockMid + 1 + textLength] = -textInPi[::-1]

        # re compute  the ophase amtrix
        for i in range(1, len(phase)):
            phase[i] = phase[i - 1] + phaseDiffs[i - 1]

        # apply i-dft
        blocks = (magnitudes * np.exp(1j * phase))
        blocks = np.fft.ifft(blocks).real

        # combining all block of audio again
        self.audioData[0] = blocks.ravel().astype(np.int16)

        return self.save(self.audioData.T, location)

    def decodeAudio(self, location) :

        self.ConvertToByte(location)
        textLength = 800
        blockLength = 2 * int(2 ** np.ceil(np.log2(2 * textLength)))
        blockMid = blockLength // 2

        # get header info
        if len(self.audioData.shape) == 1:
            x = self.audioData[:blockLength]
        else:
            x = self.audioData[:blockLength, 0]

        # get the phase and convert it to binary
        secretPhases = (np.angle(np.fft.fft(x))[blockMid - textLength:blockMid]<0).astype(np.int8)

        #  convert into characters
        secretInIntCode = secretPhases.reshape((-1, 8)).dot(1 << np.arange(8 - 1, -1, -1))

        # combine characters to original text
        return "".join(np.char.mod("%c", secretInIntCode)).replace("~", "")

    def save(self, audionew, location):
        # save file
        direction = os.path.dirname(location)
        sp.io.wavfile.write(direction + "/AudioPhase.wav", self.rate, audionew)
        return direction + "/AudioPhase.wav"


