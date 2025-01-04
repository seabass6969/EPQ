import spectrogram_analysis
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

data, sample_rate = spectrogram_analysis.LoadFile("songs/dance_of_the_sugar_plum_fairy.ogg")
t = np.linspace(0, 20, data.shape[0])
y = np.sin(5000 * t)

result = data + y
wavfile.write("simple_sugar.wav", sample_rate, result)