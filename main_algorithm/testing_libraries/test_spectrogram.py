import settings
import librosa
import scipy.io
import scipy.signal
import matplotlib.pyplot as plt
import numpy
import scipy.ndimage

sample_rate, samples = scipy.io.wavfile.read("/tmp/0f0d9e17-a8f7-43c4-824d-399ea41da63c.wav")
print(len(samples))
nperseg = min(256, len(samples))
f, t, spec = scipy.signal.spectrogram(samples, sample_rate)
print(spec.shape)
filtered_spec = scipy.ndimage.maximum_filter(spec,size=settings.box_size, mode="constant", cval=0)

boolMask = (spec == filtered_spec)
print(boolMask.shape)

spec_times, frequency = boolMask.nonzero()
print(spec_times)
