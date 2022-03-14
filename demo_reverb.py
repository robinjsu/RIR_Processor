from ir_module import wav_util, default
from ir_module.Signal import Signal
import numpy as np
import pyaudio

seconds = 5
params, ir = wav_util.read_wave_nbit('demo/impulse_responses/garage_rir_nospkr_nocover.wav')
start = np.argmax(ir)

impulse = ir[start:start+(default.sample_rate * seconds)]
impulse = np.append(np.zeros(1000), impulse)
# impulse = impulse * .5 # scale impulse to avoid clipping (which can cause pops in audio playback)
ibytes = wav_util.samples_to_bytes_16bit(impulse)

params, dry_audio = wav_util.read_wave_nbit('demo/dry_audio/bach_prelude_mono.wav')
audio = Signal(dry_audio, params.framerate, params.nchannels, params.sampwidth)
rir = Signal(impulse, params.framerate, params.nchannels, params.sampwidth)

conv = audio.convolve(rir)

wav_util.play_wav_16bit(conv, params.framerate, params.nchannels, pyaudio.paInt16)
# wav_util.write_wav_file_16bit('bach-reverb.wav', conv, 1, 48000, 2)

