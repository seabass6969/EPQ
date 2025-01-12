import spectrogram_analysis
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

def basic_noise(input, output):
    sample_rate, data = spectrogram_analysis.LoadFile(input)
    t = np.linspace(0, 20, data.shape[0])
    y = np.sin(5000 * t)

    result = data + y
    wavfile.write(output, sample_rate, result)

def random_noise(input, output):
    sample_rate, data = spectrogram_analysis.LoadFile(input)

    rng = np.random.default_rng()
    N = data.shape[0]
    amp = 2 * np.sqrt(2)
    noise_power = 0.01 * sample_rate / 2
    time = np.arange(N) / float(sample_rate)
    mod = 500*np.cos(2*np.pi*0.25*time)
    carrier = amp * np.sin(2*np.pi*3e3*time + mod)
    noise = rng.normal(scale=np.sqrt(noise_power), size=time.shape)
    noise *= np.exp(-time/5)
    result = data + carrier + noise
    wavfile.write(output, sample_rate, result)

random_noise("gymnopedie.mp3", "gymnopedie_noised.wav")
# wholely inspired by https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html
