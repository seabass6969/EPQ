import matplotlib.pyplot as plt
import numpy as np
import librosa
from scipy.ndimage import maximum_filter

file = librosa.example("brahms")
data, sample_rate = librosa.load(file, sr=None)

n_mels = 128
S = librosa.feature.melspectrogram(y=data, n_mels=n_mels)
S_db = librosa.power_to_db(S, ref=np.max)
# rows, cols = numpy.where(peaks)

# fig, ax = plt.subplots(nrows=1, sharex=True, sharey=True, figsize=(10, 10))
imgc = librosa.display.specshow(S_db, y_axis="mel", x_axis="time")
# imgd = librosa.display.specshow(S, y_axis="mel", x_axis="time", ax=ax[1])
# imge = librosa.display.specshow(local_max, y_axis="mel", x_axis="time", ax=ax[2])


peaks = []
for row in S_db:
    row_peaks = librosa.util.peak_pick(row, pre_max=3, post_max=3, pre_avg=5, post_avg=5, delta=5, wait=0)
    peaks.append(row_peaks)

for mel_band, peak_indices in enumerate(peaks):
    plt.scatter(peak_indices, [mel_band] * len(peak_indices), color='cyan', s=2, zorder=5)

plt.show()