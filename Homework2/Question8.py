from matplotlib import pyplot as plt
import numpy as np 
import scipy

#Frequency in terms of Hertz
fre  = 5 
#Sample rate
fre_samp = 50
t = np.linspace(0, 2, 2 * fre_samp, endpoint = False )
a = np.sin(fre  * 2 * np.pi * t)
figure, (axis1, axis2) = plt.subplots(1, 2)
axis1.plot(t, a)
axis1.set_xlabel ('Time (s)')
axis1.set_ylabel ('Signal amplitude')
axis1.set_title("original signal")
# plt.show()

#do DFT and visualize:
af = scipy.fft.fft(a)
t_at = np.linspace(0, fre/2, fre_samp)
axis2.plot(t_at, np.abs(af[:fre_samp]))
axis2.set_title("dft signal")
plt.show()
