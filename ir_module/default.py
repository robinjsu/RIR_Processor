import numpy as np

sample_rate = 48000              # samples per second
frequency = 1000                 # Hz
upsample_rate = sample_rate * 2  # samples per second
channels = 1                     # mono(1), stereo(2), etc.
sample_width = 2                 # frame size in bytes
amplitude = 0.75                 # floating-point between 0 and 1

sec_of_audio = 5
ir_dir = 'ir'                    # directory name for impulse responses
sweep_dir = 'sweep'              # directory name for sine sweeps

two_pi = 2 * np.pi               # regularly-used constants
fft_sz = 4096