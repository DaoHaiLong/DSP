from lap1 import Input_1kHz_15kHz, X
import matplotlib.pyplot as plt
from scipy import fftpack
import numpy as np

Impulse_response = [
  -0.0018225230, -0.0015879294, +0.0000000000, +0.0036977508, +0.0080754303, +0.0085302217, -0.0000000000, -0.0173976984,
  -0.0341458607, -0.0333591565, +0.0000000000, +0.0676308395, +0.1522061835, +0.2229246956, +0.2504960933, +0.2229246956,
  +0.1522061835, +0.0676308395, +0.0000000000, -0.0333591565, -0.0341458607, -0.0173976984, -0.0000000000, +0.0085302217,
  +0.0080754303, +0.0036977508, +0.0000000000, -0.0015879294, -0.0018225230
]
#-------------------------------------------------- System--------------------------------------------------------------
plt.title('system')
plt.plot(Impulse_response)
plt.show()

H = fftpack.fft(Impulse_response)
f_s = 100 
freqs = fftpack.fftfreq(len(Impulse_response)) * f_s
fig, ax = plt.subplots()
ax.stem(freqs, np.abs(H))
ax.set_xlim(-f_s / 2, f_s / 2)
plt.title('frequency')
plt.show()

    #------inverse-----
y=fftpack.ifft(H)
fs=44100
N2=len(H)
dt2=1/fs
plt.title('inverse_System')
plt.plot(y)
plt.show()

  #--------real--------

plt.title('real_system')
plt.plot(np.real(H))
plt.show()
 #-------- imaginary------
plt.title('imaginary_system')
plt.plot(np.imag(H))
plt.show()
  #---------magnitude--------
plt.title('magnitude_system')
plt.plot(np.abs(H))
plt.show()
  #------------phase------
plt.title('phase_system')
plt.plot(np.angle(H))
plt.show()  


#------------------Convolution-----------
output_convolution=np.convolve(Impulse_response,Input_1kHz_15kHz)
print(len(output_convolution))
plt.title('convolution')
plt.plot(output_convolution)
plt.show()

#-----------------------frequency multiplication----------------
def padding_array(array, length):
    t = length - len(array)
    return np.pad(array, pad_width=(0, t), mode='constant')
padding=padding_array(Impulse_response,len(Input_1kHz_15kHz))
new_padding=fftpack.fft(padding)
freq_multi=np.multiply(X,new_padding)
print(len(freq_multi))
plt.title('frequency multiplication')
plt.plot(freq_multi)
plt.show()