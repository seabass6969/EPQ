import math
import os
# import librosa
# import librosa.display
import numpy as np
from scipy.ndimage import maximum_filter
from scipy.signal import spectrogram
import matplotlib.pyplot as plt
import settings as settings
import database
import searching
from pydub import AudioSegment

# Load an audio file and compute a Mel spectrogram

np.set_printoptions(precision=3, suppress=True)

def LoadFile(file_name: str):
    """
    :param file_name the file name with it's relative location where the program is ran
    :return: data, sample_rate
    """
    file = os.path.join("", file_name)
    audioFile = AudioSegment.from_file(file).set_channels(1).set_frame_rate(settings.sample_rate)
    return np.frombuffer(audioFile.raw_data, np.int16)
    # return librosa.load(file, sr=settings.sample_rate)
    # Depracated Code

# def ProduceFilteredSpectrogram(data):
    # from scipy.signal import spectrogram
    # nperseg = int(settings.sample_rate * settings.fft_window_size)
    # S = spectrogram(data, settings.sample_rate, nperseg=nperseg)
    
    # S = librosa.feature.melspectrogram(
    #     y=data, sr=sample_rate, n_mels=settings.n_mels, hop_length=settings.hop_length
    # )
    # mel = librosa.decompose.nn_filter(S)
    # mel = maximum_filter(S, size=30, mode="constant", cval=0.0)

def convertTFtorealTF(coordinates, t,f):
    """
        :param coordinates: list of coordinates formatted originally in (time, frequency) but in index location form
        :param t: list of time index location from scipy.signal.spectrogram
        :param f: list of frequency index location from scipy.signal.spectrogram

        :returns: Returns original location values of (time, frequency)
    """
    return np.array([(f[i[0]], t[i[1]] ) for i in coordinates])

def getPeaks(data):
    frequencies, time, spec = spectrogram(data, settings.sample_rate)
    filtered_spectrogram = maximum_filter(spec, size=settings.box_size, mode="constant", cval=0.0)
    peak_boolean_mask = (spec == filtered_spectrogram)
    peak_y, peak_x = peak_boolean_mask.nonzero()
    peak_values = spec[peak_y, peak_x]
    indexes = peak_values.argsort()[::-1] # reversed sorted index
    j = [(peak_y[idx], peak_x[idx]) for idx in indexes]
    total_peaks = spec.shape[0] * spec.shape[1]
    peak_target = int((total_peaks / (settings.box_size ** 2)) * settings.point_efficiency)
    real_j = convertTFtorealTF(j[:peak_target], time, frequencies)
    if settings.PRODUCE_DIAGRAM:
        figs, axs = plt.subplots(2)
        axs[0].pcolormesh(time, frequencies, spec, shading="auto")
        axs[1].pcolormesh(time, frequencies, filtered_spectrogram, shading="auto")
        x,y = real_j.T
        axs[1].scatter(y, x, color="cyan", s=2)
        
        plt.show()
    return real_j
    # peak_x = []
    # peak_y = []
    # all_peaks = []  # keys - time  value - Frequency

    # mel_frequencies = librosa.mel_frequencies(
    #     n_mels=spectrogram.shape[0], fmin=0, fmax=sample_rate // 2
    # )
    # for row in range(spectrogram.shape[0]):  # Iterate over each frequency bin (row)
    #     row_peaks = librosa.util.peak_pick(
    #         spectrogram[row, :],
    #         pre_max=3,
    #         post_max=3,
    #         pre_avg=5,
    #         post_avg=5,
    #         delta=10,
    #         wait=0,
    #     )
    #     for peak in row_peaks:
    #         # Convert peaks to x (time in seconds) and y (frequency in Hz) coordinates
    #         time = peak * settings.hop_length / sample_rate
    #         Hz_frequency = mel_frequencies[row]
    #         all_peaks.append((time, Hz_frequency))

    #         if settings.PRODUCE_DIAGRAM:
    #             peak_x.append(time)  # Time in seconds
    #             peak_y.append(Hz_frequency)  #  Frequency in Hz

    # if settings.PRODUCE_DIAGRAM:
    #     plt.figure(figsize=(10, 4))
    #     librosa.display.specshow(
    #         spectrogram,
    #         sr=sample_rate,
    #         hop_length=settings.hop_length,
    #         x_axis="time",
    #         y_axis="mel",
    #         cmap="magma",
    #     )
    #     plt.colorbar()

    #     # Overlay peaks using scatter
    #     plt.scatter(peak_x, peak_y, color="cyan", s=2)
    #     plt.title("Mel Spectrogram with Peaks")
    #     plt.tight_layout()
    #     plt.show()
    # return all_peaks


# anchor point picking


def getTargetZonePoints(points, anchor_point):
    """
        Generate Points from the target Zone.
    """
    t_min = anchor_point[1] + settings.ACTUAL_TIME_GAP
    t_max = anchor_point[1] + settings.ACTUAL_THRESHOLD_TIME_DISTANCE
    f_min = anchor_point[0] - (settings.FREQUENCY_HEIGHT_LIMIT / 2)
    f_max = anchor_point[0] + (settings.FREQUENCY_HEIGHT_LIMIT / 2)
    for point in points:
        if point[1] >= t_min and point[1] <= t_max and point[0] >= f_min and point[0] <= f_max:
            yield point


def hashPoints(pointA, pointB):
    # return hash(
    #     (
    #         pointA[0].item(),
    #         pointB[0].item(),
    #         (pointB[1] - pointA[1]).item(),
    #     )
    # )
    return hash(
        (
            round(pointA[0].item(), 1),
            round(pointB[0].item(), 1),
            round((pointB[1] - pointA[1]).item(), 1),
        )
    )



def searchPairs(song_file):
    """
    :return generator function of (time_deltas, hashes)
    """
    data = LoadFile(song_file)
    peaks = getPeaks(data)
    print(len(peaks))
    for anchor_point in peaks:
        for target_point in getTargetZonePoints(peaks, anchor_point):
            yield (target_point[1] - anchor_point[1], hashPoints(anchor_point, target_point))

def getPairs(song_file, uuids):
    data = LoadFile(song_file)
    peaks = getPeaks(data)
    print(len(peaks))
    for anchor_point in peaks:
        for target_point in getTargetZonePoints(peaks, anchor_point):
            yield (hashPoints(anchor_point, target_point), uuids, anchor_point[1].item())
    # spectrogram = ProduceFilteredSpectrogram(data, sample_rate)

    # points = getPeaks(spectrogram, sample_rate)
    # print(len(points))
    # for anchor_point in points:
    #     targetZone = getTargetZonePoints(points, anchor_point)
    #     for target_point in targetZone:
    #         total_pairs.append(
    #             (
    #                 hashPoints(anchor_point, target_point),
    #                 round(anchor_point[0].item(), 1),
    #                 uuids,
    #             )
    #         )


if __name__ == "__main__":
    # pairs = list(getPairs("songs/brahm.ogg", "asdasdasdqasd"))
    # print(len(pairs))
    # data, sample_rate = LoadFile("songs/brahm.ogg")
    # spectrogram = ProduceFilteredSpectrogram(data, sample_rate)
    # points = getPeaks(spectrogram, sample_rate)
    # print(len(points))
    pass
