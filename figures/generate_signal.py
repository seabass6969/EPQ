import numpy as np
from matplotlib import pyplot as plt

SAMPLE_RATE = 44100  # Hertz
DURATION = 60  # Seconds

def generate_sine_wave(freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    # 2pi because np.sin takes radians
    y = np.sin((2 * np.pi) * frequencies)
    return x, y

# Generate a 2 hertz sine wave that lasts for 5 seconds
_, mixed_tone = generate_sine_wave(659, SAMPLE_RATE, DURATION)
normalized_tone = np.int16((mixed_tone / mixed_tone.max()) * 32767)

from scipy.io.wavfile import write
write("E_659.wav", SAMPLE_RATE, normalized_tone)

