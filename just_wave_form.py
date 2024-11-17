import numpy as np
import os
from scipy.io import wavfile
import matplotlib.pyplot as plt

# all calculated in radian
# await function to convert audio file from stereo to mono
samplerate, data = wavfile.read(os.path.join("", "mono.wav"))
length = data.shape[0] / samplerate
time = np.linspace(0, length, data.shape[0])
plt.plot(time, data)
plt.legend()
# Nyquist theorem

plt.show()