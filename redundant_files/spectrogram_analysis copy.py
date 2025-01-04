import math
import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

# Load an audio file and compute a Mel spectrogram
file = librosa.example("brahms")
# file = os.path.join("", "new_brahm.wav")
y, sr = librosa.load(file, sr=None)
n_fft = 2048
hop_length = 512
# hop length = the number of samples between the start of two consecutive windows in the signal windowing
S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, hop_length=hop_length)
mel = librosa.decompose.nn_filter(S)

mel_frequencies = librosa.mel_frequencies(n_mels=mel.shape[0], fmin=0, fmax=sr // 2)
peak_x = []
peak_y = []

THRESHOLD_TIME_DISTANCE = 3
ACTUAL_THRESHOLD_TIME_DISTANCE = THRESHOLD_TIME_DISTANCE * hop_length / sr
FREQUENCY_HEIGHT_LIMIT = 500
all_peaks = []  # (peak_strength, time_second, hertz_frequency)
bonk = 0
for column in range(mel.shape[1]):  # Iterate over each time (columns)
    column_peaks = librosa.util.peak_pick(
        mel[:, column], pre_max=3, post_max=3, pre_avg=5, post_avg=5, delta=10, wait=0
    )
    # x 0 0
    # x 0 0
    awaiting_sort_row = []
    for peak in column_peaks:
        # Convert peaks to x (time in seconds) and y (frequency in Hz) coordinates
        time = column * hop_length / sr
        Hz_frequency = mel_frequencies[peak]
        awaiting_sort_row.append((mel[peak, column], time, Hz_frequency))
        peak_x.append(time)  # Time in seconds
        peak_y.append(Hz_frequency)  #  Frequency in Hz
        bonk += 1
    awaiting_sort_row.sort(key=lambda x: x[0])
    all_peaks.append(awaiting_sort_row)


plt.figure(figsize=(10, 4))
librosa.display.specshow(
    mel, sr=sr, hop_length=hop_length, x_axis="time", y_axis="mel", cmap="magma"
)
plt.colorbar()

# Overlay peaks using scatter
plt.scatter(peak_x, peak_y, color="cyan", s=2)
plt.title("Mel Spectrogram with Peaks")
plt.tight_layout()
plt.show()

# anchor point picking
def indentify_pairs(item, next_rows_items):
    results = []
    item_frequency = item[2]
    item_time = item[1]
    filtration = filter(lambda x: (x[2] < (FREQUENCY_HEIGHT_LIMIT + item_frequency) and (x[2] > (FREQUENCY_HEIGHT_LIMIT - item_frequency))), next_rows_items)
    for filtered_item in filtration:
        results.append((item_frequency, filtered_item[2], filtered_item[1] - item_time))
    return results

# pairs = indentify_pairs(all_peaks[0][1], np.array(all_peaks[2: 10]).flatten())

def flatten(iterable):
    resulting_array = []
    for i in iterable:
        resulting_array.extend(i)
    return resulting_array

total_pairs = []
for index, peaks in enumerate(all_peaks[:len(all_peaks) - TIME_GAP - THRESHOLD_TIME_DISTANCE]):
    if len(peaks) != 0:
        best_peaks_row = peaks
        next_rows = flatten(all_peaks[index + TIME_GAP : index + TIME_GAP + THRESHOLD_TIME_DISTANCE])
        for peak in best_peaks_row:
            pairs = indentify_pairs(peak, next_rows)
            total_pairs.extend(pairs)

# print(total_pairs)
print(len(total_pairs))

# print(bonk)