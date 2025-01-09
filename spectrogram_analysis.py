import math
import os
# import librosa
# import librosa.display
import numpy as np
from scipy.ndimage import maximum_filter
import librosa
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
    data, sample_rate = librosa.load(file, sr=settings.sample_rate)
    print(sample_rate)
    return data

def convertTFtorealTF(coordinates, f):
    """
        :param coordinates: list of coordinates formatted originally in (time, frequency) but in index location form
        :param t: list of time index location from scipy.signal.spectrogram
        :param f: list of frequency index location from scipy.signal.spectrogram

        :returns: Returns original location values of (time, frequency)
    """
    return np.array([(i[1] * settings.hop_length / settings.sample_rate, f[i[0]]) for i in coordinates])

def getPeaks(data):
    spec, frequencies = createSpectrogram(data)
    filtered_spectrogram = maximum_filter(spec, size=settings.box_size, mode="constant", cval=0)
    peak_boolean_mask = (spec == filtered_spectrogram)
    peak_times, peak_frequencies = peak_boolean_mask.nonzero()
    peak_values = spec[peak_times, peak_frequencies]
    indexes = peak_values.argsort()[::-1] # reversed sorted index
    # sorting power level from the largest to the smallest
    j = [(peak_times[idx], peak_frequencies[idx]) for idx in indexes]
    # j: (time, frequency)
    total_peaks = spec.shape[0] * spec.shape[1]
    peak_target = int((total_peaks / (settings.box_size ** 2)) * settings.point_efficiency)
    # real_j = convertTFtorealTF(j[:peak_target], frequencies)
    real_j = convertTFtorealTF(j, frequencies)
    print(real_j)
    print("Max time: ", max(real_j[:,0]))
    print("Max Frequency: ",max(real_j[:,1]))
    if settings.PRODUCE_DIAGRAM:
        figs, axs = plt.subplots(2, sharex=True, sharey=True)
        img = librosa.display.specshow(spec, x_axis='time', y_axis='linear',ax=axs[0])
        # figs.colorbar(img, ax=axs)
        # img = librosa.display.specshow(filtered_spectrogram, x_axis='time', y_axis='linear', ax=axs[1])
        # axs[0].pcolormesh(time, frequencies, spec, shading="auto")
        # axs[1].pcolormesh(time, frequencies, filtered_spectrogram, shading="auto")
        x,y = real_j.T
        axs[0].scatter(x, y, color="lime", s=2)
        
        plt.show()
    return real_j


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
            yield (round(target_point[1] - anchor_point[1], 1), hashPoints(anchor_point, target_point))

def getPairs(song_file, uuids):
    data = LoadFile(song_file)
    peaks = getPeaks(data)
    if settings.DEBUG:
        print(len(peaks))
    for anchor_point in peaks:
        for target_point in getTargetZonePoints(peaks, anchor_point):
            yield (hashPoints(anchor_point, target_point), uuids, round(anchor_point[1].item(), 1))

def createSpectrogram(data):
    """
        :return ([(n_mels, time)], mel_frequencies)
    """
    mel = librosa.feature.melspectrogram(y=data, sr=settings.sample_rate, n_mels=settings.n_mels, hop_length=settings.hop_length)
    print(mel.shape)
    mel_frequency = librosa.mel_frequencies(n_mels=mel.shape[0], fmin=0, fmax=(settings.sample_rate))
    # times = [t * settings.hop_length / settings.sample_rate for t in range(mel.shape[1])]
    return mel, mel_frequency

if __name__ == "__main__":
    peaks = getPeaks(LoadFile("./songs/dance_of_the_sugar_plum_fairy.ogg"))
    print(len(peaks))
    pass
