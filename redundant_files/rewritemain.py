import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from PIL import Image
import seaborn as sns

import librosa
import librosa.display

import skimage.io

# raw_audio, sample_rate = librosa.load("mono.wav")
raw_audio, sample_rate = librosa.load(librosa.example("brahms"))
print(f"sample rate: {sample_rate}")

series = pd.Series(raw_audio)
# plotting just the raw audio 
# series.plot(figsize=(10, 5), lw=1, title="raw audio")

audio_array = librosa.stft(raw_audio)
S_db = librosa.amplitude_to_db(np.abs(audio_array), ref=np.max)

# ax = plt.subplot()
# img = librosa.display.specshow(audio_array, x_axis='time', y_axis="log")
FFT_WINDOWING = 2**12
# melImg_spec = librosa.feature.melspectrogram(y=raw_audio, sr=sample_rate, n_fft=FFT_WINDOWING)[0]
# melImg_spec = np.log(melImg_spec + 1e-10)
# melImg= scale_minmax(melImg_spec, 0, 2**16 - 1).astype(np.uint16)

# melImg= np.flip(melImg, axis=0)
# melImg= 255-melImg # make black
# plt.colorbar(img, ax=ax, format=f'%0.2f')

# plt.show()


print()
# image = Image.fromarray(melImg_spec, "RGB")
# image.save("out.png")

# skimage.io.imsave("out.png", melImg_spec)
