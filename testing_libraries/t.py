import librosa

# Load the audio
y, sr = librosa.load("songs/dance_of_the_sugar_plum_fairy.ogg", sr=None)

# Compute the spectrogram
n_fft = 2048
hop_length = 512
S = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)

# Get the time array for the spectrogram
time_indices = range(S.shape[1])  # Time indices (columns in the spectrogram)
time_values = librosa.frames_to_time(time_indices, sr=sr, hop_length=hop_length)

print("Time values for each time bin:", time_values)
from scipy.ndimage import maximum_filter
import numpy as np

# Detect peaks (example boolean mask for peaks)
S = librosa.amplitude_to_db(np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length)), ref=np.max)
filtered_S = maximum_filter(S, size=5)
peak_mask = (S == filtered_S)
peak_times, _ = np.nonzero(peak_mask)  # Get time indices of peaks

# Convert time indices to real time
real_times = librosa.frames_to_time(peak_times, sr=sr, hop_length=hop_length)

print("Real time values for peaks:", real_times)
