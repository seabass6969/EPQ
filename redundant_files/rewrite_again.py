from skimage.feature import peak
import matplotlib.pyplot as plt
import librosa.display
import sys
import librosa.feature
import numpy
from scipy import signal

numpy.set_printoptions(threshold=sys.maxsize)

# file = librosa.example("brahms")
file = librosa.ex("trumpet")

data, sample_rate = librosa.load(file)
duration = len(data) / sample_rate
n_mels = 128
fmax = 8000
melspectrogram = librosa.feature.melspectrogram(
    y=data, sr=sample_rate, n_mels=n_mels, fmax=fmax
)
mel = librosa.decompose.nn_filter(melspectrogram)

# y_line = numpy.linspace(0, len(mel) - 1)
fig, ax = plt.subplots(nrows=3, sharex=True, sharey=True, figsize=(10, 10))
imgc = librosa.display.specshow(melspectrogram, y_axis="mel", x_axis="time", ax=ax[0])
imgd = librosa.display.specshow(mel, y_axis="mel", x_axis="time", ax=ax[1])
imge = librosa.display.specshow(mel, y_axis="mel", x_axis="time", ax=ax[2])

# total_peaks = []
actual_peaks = librosa.util.peak_pick(
    mel.mean(axis=0), pre_max=3, post_max=3, pre_avg=10, post_avg=10, delta=0.1, wait=1
)
actual_peaks_time = librosa.frames_to_time(actual_peaks, sr=sample_rate)
x_peaks = []
y_peaks = []
# for index, x in enumerate(mel):
#     peaks = librosa.util.peak_pick(x, pre_max=3, post_max=3, pre_avg=3, post_avg=3, delta=0.5, wait=10)
#     if len(peaks) > 0:
#         for peak in peaks:
#             x_peaks.append(index)
#             y_peaks.append(peak)
mel_frequencies = librosa.mel_frequencies(n_mels=n_mels, fmin=0, fmax=fmax)

for index, x in enumerate(actual_peaks_time):
    rows = mel[actual_peaks[index]]
    # mean_value = rows.mean()
    # for indexrow,item in enumerate(rows):
    #     if item > mean_value:
    #         x_peaks.append(x)
    #         y_peaks.append(mel_frequencies[indexrow])
    split = librosa.util.peak_pick(rows, pre_max=3, post_max=3, pre_avg=10, post_avg=10, delta=0.1, wait=1)
    for i in split:
        # print(actual_peaks[index])
        x_peaks.append(x)
        y_peaks.append(mel_frequencies[i - 1])
        # ax[2].hlines(i, xmin=0, xmax=100, colors="#ffffff")


# ax[2].vlines(actual_peaks_time, ymin=0, ymax=10000, colors="#ffffff")
# print(x_peaks)
# print(y_peaks)
ax[2].scatter(x_peaks, y_peaks)

# print(peaks)

# imge = librosa.display.specshow(fil, y_axis='mel', x_axis='time', ax=ax[2])
fig.colorbar(imgc, ax=ax[:3])

plt.show()
