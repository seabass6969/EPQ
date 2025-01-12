import os
import numpy as np
from scipy.ndimage import maximum_filter
from scipy.signal import spectrogram
import matplotlib.pyplot as plt
import settings as settings
import database
import searching
from pydub import AudioSegment
from scipy.io import wavfile
import ffmpeg
import re
import uuid
import hashlib
from typing import Tuple

# Load an audio file and compute a Mel spectrogram

np.set_printoptions(precision=3, suppress=True)

def LoadFile(file_name: str, file_start: str = ""):
    """
        :param file_name the file name with it's relative location where the program is ran
        :return: data, sample_rate
    """
    file = os.path.join(file_start, file_name)
    # data, sample_rate = librosa.load(file, sr=settings.sample_rate)
    # if file_name.endswith(".wav"):
        #sample_rate, audio = wavfile.read(file)
        #return sample_rate, audio
    #else: 
    new_file = f"{uuid.uuid4()}.wav"
    # new_file = re.sub(r"(\..*)", '.wav', file_name)
    new_format = os.path.join("/tmp", new_file)
    if settings.DEBUG:
        print(new_format)
        os.system(f"ffmpeg -y -i '{file}' -ac 1 '{new_format}'")
    else:
        os.system(f"ffmpeg -loglevel quiet -y  -i '{file}' -ac 1 '{new_format}'")
    # ffmpeg.input(file).output(new_format).run()
    sample_rate, audio = wavfile.read(new_format)
    return sample_rate, audio

def convertTFtorealTF(coordinates, f, t):
    """
        :param coordinates: list of coordinates formatted originally in (time, frequency) but in index location form
        :param t: list of time index location from scipy.signal.spectrogram
        :param f: list of frequency index location from scipy.signal.spectrogram

        :returns: Returns original location values of (time, frequency)
    """
    return np.array([(f[i[0]], t[i[1]]) for i in coordinates])

def getPeaks(data, sample_rate):
    f, t, spec = createSpectrogram(data, sample_rate=sample_rate)
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
    real_j = convertTFtorealTF(j[:peak_target], f, t)
    # real_j = convertTFtorealTF(j, f, t)
    if settings.DEBUG:
        print(peak_values)
        print(real_j)
        print("Max time: ", max(real_j[:,1]))
        print("Max Frequency: ",max(real_j[:,0]))
    # mm = [real_j for s in real_j if real_j[0] > 100]
    # print("Max Frequencies' power value: ", )
    if settings.PRODUCE_DIAGRAM:
        _, axs = plt.subplots(2, sharex=True, sharey=True)
        axs[0].pcolormesh(t, f, spec, shading="gouraud")
        axs[1].pcolormesh(t, f, filtered_spectrogram, shading="gouraud")
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [s]')
        y,x = real_j.T
        axs[0].scatter(x, y, color="lime", s=2)
        axs[1].scatter(x, y, color="lime", s=2)
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


def hasher(tuples: Tuple[str, str, str]):
    return hashlib.sha512(",".join(tuples).encode("utf-8")).hexdigest()

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
            (pointA[0].item()),
            (pointB[0].item()),
            ((pointB[1] - pointA[1]).item()),
        )
    )


def searchPairs(song_file, file_start):
    """
    :return generator function of (time_deltas, hashes)
    """
    sample_rate, data = LoadFile(song_file, file_start)
    peaks = getPeaks(data, sample_rate)
    print(len(peaks))
    for anchor_point in peaks:
        for target_point in getTargetZonePoints(peaks, anchor_point):
            yield (round(target_point[1] - anchor_point[1], 1), hashPoints(anchor_point, target_point))

def getPairs(song_file, file_start, uuids):
    sample_rate, data = LoadFile(song_file, file_start)
    peaks = getPeaks(data, sample_rate)
    if settings.DEBUG:
        print(len(peaks))
    for anchor_point in peaks:
        for target_point in getTargetZonePoints(peaks, anchor_point):
            yield (hashPoints(anchor_point, target_point), uuids, round(anchor_point[1].item(), 1))

def createSpectrogram(audio, sample_rate):
    """
        :return ([(n_mels, time)], mel_frequencies)
    """
    nperseg = int(sample_rate * settings.fft_window_size)
    return spectrogram(audio, sample_rate, nperseg = nperseg)

if __name__ == "__main__":
    pairs = getPairs('38 Kevin MacLeod - Lift Motif.mp3', "songs/Kevin_MacLeod_Classical_sampler", "123123123123")
    print(len(list(pairs)))
    # print(len(peaks))
    
    pass
