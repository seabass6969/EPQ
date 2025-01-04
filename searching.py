import database
import settings
import spectrogram_analysis
import numpy
import matplotlib.pyplot as plt


def scoring_song(time_offsets):
    time_gap = 0.5
    bin = numpy.arange(int(min(time_offsets)), int(max(time_offsets)) + 1 + time_gap)
    counts, bins = numpy.histogram(time_offsets, bins=bin)
    print(time_offsets)
    # plt.stairs(counts, bins)
    # plt.show()
    return numpy.max(counts)

def searching(file_name):
    deltas_hashes = list(spectrogram_analysis.searchPairs(file_name))
    print(len(deltas_hashes))
    songs_dict = database.search_points(deltas_hashes)
    # this returns the original offsets to the song
    song_scores = {}
    for time_offsets in songs_dict.items():
        song_scores[time_offsets[0]] = scoring_song(time_offsets[1])
    print(song_scores)
    max_song = max(song_scores, key=lambda x: song_scores[x])
    return database.get_entry(max_song)


if __name__ == "__main__":
    matched = searching("test/shifted_sugar.wav")
    print(matched)
# "songs/dance_of_the_sugar_plum_fairy.ogg"
