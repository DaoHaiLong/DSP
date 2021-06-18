from abc import ABC, abstractmethod


# abstract class for a  audio steganography algorithm

class Audio(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def encodeAudio(self, location, text) :
        pass

    @abstractmethod
    def decodeAudio(self, location) :
        pass

    @abstractmethod
    def ConvertToByte(self, audio):
        pass
    
    @abstractmethod
    def ConvertToByte(self, location):
        pass

    @abstractmethod
    def save(self, audionew, location) :
        pass