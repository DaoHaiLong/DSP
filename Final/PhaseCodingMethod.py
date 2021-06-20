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

        blockchannelLength = int(2 * 2 ** np.ceil(np.log2(2 * textLength)))
        blockchannelNumber = int(np.ceil(self.audioData.shape[0] / blockchannelLength))

        # checks shape to change data to 1 axis
        if len(self.audioData.shape) == 1:
            self.audioData.resize(blockchannelNumber * blockchannelLength, refcheck=False)
            self.audioData = self.audioData[np.newaxis]
        else:
            self.audioData.resize((blockchannelNumber * blockchannelLength, self.audioData.shape[1]), refcheck=False)
            self.audioData = self.audioData.T

        blockchannel = self.audioData[0].reshape((blockchannelNumber, blockchannelLength))

        # Calculate DFT using fft
        blockchannel = np.fft.fft(blockchannel)
        
         # create phase matrix
        phase = np.angle(blockchannel)
        # get phase differences
        phaseDiff = np.diff(phase, axis=0)

        # calculate magnitudes
        magnitudes = np.abs(blockchannel)

        # conert message to encode into binary
        textInToBinary = np.ravel([[int(y) for y in format(ord(x), "08b")] for x in text])

        # Convert txt to phase differences
        textCovertPhasePi = textInToBinary.copy()
        textCovertPhasePi[textCovertPhasePi == 0] = -1
        textCovertPhasePi =textCovertPhasePi * -np.pi / 2
        # calc block channel mid
        blockChannelMid = blockchannelLength // 2
        # do phase conversion
        phase[0, blockChannelMid - textLength: blockChannelMid] =textCovertPhasePi
        phase[0, blockChannelMid + 1: blockChannelMid + 1 + textLength] = -textCovertPhasePi[::-1]

        # re compute  the ophase amtrix
        for i in range(1, len(phase)):
            phase[i] = phase[i - 1] + phaseDiff[i - 1]

        # apply i-dft(using ifft to covert )
        blockchannel = (magnitudes * np.exp(1j * phase))
        blockchannel = np.fft.ifft(blockchannel).real
        # combining all block of audio again
        self.audioData[0] = blockchannel.ravel().astype(np.int16)
        return self.save(self.audioData.T, location)

    def decodeAudio(self, location) :
        
        self.ConvertToByte(location)
        textLength = 800
        blockchannelLength = 2 * int(2 ** np.ceil(np.log2(2 * textLength)))
        blockChannelMid = blockchannelLength // 2

        # get header info
        if len(self.audioData.shape) == 1:
            x = self.audioData[:blockchannelLength]
        else:
            x = self.audioData[:blockchannelLength, 0]

        # get the phase and convert it to binary
        PhasesCovertToBinary = (np.angle(np.fft.fft(x))[blockChannelMid - textLength:blockChannelMid]<0).astype(np.int8)
        #  convert into characters
        CovertToCharacters = PhasesCovertToBinary.reshape((-1, 8)).dot(1 << np.arange(8 - 1, -1, -1))
        
        # combine characters to original text
        return "".join(np.char.mod("%c", CovertToCharacters)).replace("~", "")

    def save(self, audionew, location):
        # save file
        direction = os.path.dirname(location)
        sp.io.wavfile.write(direction + "/AudioPhase.wav", self.rate, audionew)
        return direction + "/AudioPhase.wav"


