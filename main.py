import numpy as np
import os
from scipy.io import wavfile
import matplotlib.pyplot as plt
from PIL import Image

# all calculated in radian
# await function to convert audio file from stereo to mono
try:
    os.remove(os.path.join("", "myImage.png"))
except:
    pass
samplerate, data = wavfile.read(os.path.join("", "mono.wav"))
length = data.shape[0] / samplerate
time = np.linspace(0, length, data.shape[0])
noise_volts = 1*np.sin(time/(2*np.pi))

data = data + noise_volts
# length = data.shape[0] / samplerate
# time = np.linspace(0, length, data.shape[0])
# fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)
# ax1.plot(time, data)
# ax1.set_ylabel("amplitude")
# ax1.set_xlabel("time")
# Nyquist theorem
Fs = samplerate * 2  # view range
NFFT = int(Fs * 0.005)  # window length 0.005s
my_dpi = 79000
plt.figure(figsize=(data.shape[0] / my_dpi / 1000, samplerate / my_dpi /1000), dpi=my_dpi)
Pxx, freq, bins, im = plt.specgram(data, NFFT=NFFT, Fs=Fs, cmap="gray")
# plt.figure(figsize=(int(data.shape[0] ),int(samplerate )), dpi=my_dpi)

plt.axis("off")

plt.margins(0)
# matplotlib.use('Agg')

plt.savefig(
    "myImage.png",
    format="png",
    bbox_inches="tight",
    pad_inches=0,
    transparent=True,
    # dpi=my_dpi,
)


# plt.show()
# im = Image.open("myImage.png").convert("LA")
# im.show()

# im.save("myImage.png")
