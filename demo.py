from ir_module import wav_util, default, graph
from ir_module.Signal import Signal
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import pyaudio as pya

# read in WAVE files
p, sig = wav_util.read_wave_nbit('demo/recorded_output/garage/exp_30s_50-5000Hz_recorded.wav')
ip, inp = wav_util.read_wave_nbit('demo/sweeps/exp_30s_50-5000Hz_0.85-0.25amp_48000.wav')

# initialize Signal instances for ease of processing
input = Signal(inp, ip.framerate, ip.nchannels, ip.sampwidth)
out_sig = Signal(sig, p.framerate, p.nchannels, p.sampwidth)

# deconvolve input and speaker effects from recorded signal
deconvolved = out_sig.deconvolve(input)
dec_signal = deconvolved.get_signal()
# normalize signal to ensure that floating-point values are between -1 and 1 (exclusive)
overflow = np.argmax(np.abs(dec_signal))
if np.abs(dec_signal)[overflow] >= 1:
    dec_signal = dec_signal * (1/np.abs(dec_signal[overflow])) * 0.95

# plot extracted RIR
plt.plot(dec_signal)
plt.show()

# write to file
wav_util.write_wav_file_16bit('demo/impulse_responses/garage_rir.wav', dec_signal, 1, 48000, 2)