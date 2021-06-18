import os
import wave
from abstracmethod import *

class LSB(Audio):
    def ConvertToByte(self, location):
        # convert to byte array
        self.audio = wave.open(location, mode="rb")
        covert = bytearray(list(self.audio.readframes(self.audio.getnframes())))
        return covert

    def encodeAudio(self, location, text):
        # convert to array
        audioArray = self.ConvertToByte(location)
        # convert string to encode  into bit array
        text = text + int((len(audioArray) - (len(text) * 8 * 8)) / 8) * '#'
        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in text])))
        # do lsb manipulation
        for i, bit in enumerate(bits):
            audioArray[i] = (audioArray[i] & 254) | bit
        encoded = bytes(audioArray)
        return self.save(encoded, location)

    def decodeAudio(self, location):
        # reconstruct original message by converting to binary array
        audioArray = self.ConvertToByte(location)
        extracted = [audioArray[i] & 1 for i in range(len(audioArray))]
        self.audio.close()
        return \
            "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8)).split(
                "###")[0]

    def save(self, audionew, location):
        # save to dir as output-lsb
        direction = os.path.dirname(location)
        self.newAudio = wave.open(direction + "/audioStego.wav", 'wb')
        self.newAudio.setparams(self.audio.getparams())
        self.newAudio.writeframes(audionew)
        self.newAudio.close()
        self.audio.close()
        return direction + "/audioStego.wav"
