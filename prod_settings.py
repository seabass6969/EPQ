# Debug purposes only
BUILD = True
PRODUCE_DIAGRAM = False
DEBUG = False

sample_rate = 44100 
# set standard to all the sample rate 
n_mels = 40
n_fft = 2048
hop_length = 512
# hop length = the number of samples between the start of two consecutive windows in the signal windowing
FREQUENCY_HEIGHT_LIMIT = 4000
ACTUAL_THRESHOLD_TIME_DISTANCE = 1.5
# ACTUAL_THRESHOLD_TIME_DISTANCE = 1.8
ACTUAL_TIME_GAP = 0.05
# ACTUAL_TIME_GAP = 0.05
fft_window_size = 0.2
box_size = 30
# point_efficiency = 0.6
point_efficiency = 0.8
