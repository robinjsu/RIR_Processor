from ir_module import wav_util, default, graph
from ir_module.Signal import Signal
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import pyaudio as pya

# read in WAVE files
p, sig = wav_util.read_wave_nbit('demo/recorded_output/exp_30s_50-5000Hz_recorded.wav')
ip, inp = wav_util.read_wave_nbit('demo/sweeps/exp_30s_50-5000Hz_0.85-0.25amp_48000.wav')

# initialize Signal instances for ease of processing
input = Signal(inp, ip.framerate, ip.nchannels, ip.sampwidth)
out_sig = Signal(sig, p.framerate, p.nchannels, p.sampwidth)

# deconvolve input and speaker effects from recorded signal
deconvolved = out_sig.deconvolve(input)
# normalize signal to ensure that floating-point values are between -1 and 1 (exclusive)
overflow = np.argmax(np.abs(deconvolved))
if np.abs(deconvolved)[overflow] >= 1:
    deconvolved = deconvolved * (1/np.abs(deconvolved[overflow])) * 0.95


# plot extracted RIR
plt.plot(deconvolved)
plt.show()

# write to file
wav_util.write_wav_file_16bit('demo/impulse_responses/garage_rir_nospkr_nocover.wav', deconvolved, 1, 48000, 2)
