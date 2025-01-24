from scipy.fft import fft,rfft, fftfreq, rfftfreq
from matplotlib import pyplot as plt
import numpy as np

sample_rate = 1000
duration = 5

samples = sample_rate * duration
def generate_sine_wave(freq, sample_rate, duration, amplitude):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    # 2pi because np.sin takes radians
    y = np.sin((2 * np.pi) * frequencies) * amplitude
    return x, y

_,y_1 = generate_sine_wave(10, sample_rate, duration, 50)
_,y_2 = generate_sine_wave(5, sample_rate, duration, 100)
y = y_1 + y_2
normalized_y = np.int32((y / y.max()) * (2 ** 31 - 1))
yf = rfft(normalized_y)
xf = rfftfreq(samples, 1 / sample_rate)

plt.plot(xf, np.abs(yf))
plt.xlim((0, 20))
# plt.ylim((0, 80000000))
plt.show()