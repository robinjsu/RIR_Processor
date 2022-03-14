import numpy as np
from .default import *


def sine_wave(freq, duration, sample_rate=sample_rate, amp=amplitude):
    '''
    Generate single sine wave frequency for specified duration.
    :freq: frequency of sine wave in Hz
    :duration: duration of sine wave in seconds
    :sample_rate: samples per second, default=48000
    :amp: signal amplitude, default=0.75
    Returns a numpy array of normalized floating-point frames.
    '''
    def sine_func(samp):
        return amp * np.sin(two_pi * freq * ((samp % sample_rate)/ sample_rate))

    length = sample_rate * duration
    samples = np.linspace(0, length, num=length, endpoint=False)
    samples = np.array(list(map(sine_func, samples)))

    return samples

# linear sine function referenced from https://www.recordingblogs.com/wiki/sine-sweep
def lin_sweep(start, end, duration, sample_rate=sample_rate, st_amp=0.75, end_amp=0.75):
    '''
    Generate linear sine chirp, with constant amplitude over time
    :start: starting frequency (Hz)
    :end: ending frequency (Hz)
    :duration: (sec) length of sweep
    Returns a numpy array of normalized floating-point frames.
    '''
    sweep_len = sample_rate * duration
    amp_array = np.linspace(st_amp, end_amp, num=sweep_len, endpoint=True)
    sweep = np.linspace(0, sweep_len, num=sweep_len, endpoint=False)

    def sweep_func(sample):
        return amp_array[int(sample)] * np.sin(two_pi * ((start*sample/sample_rate) + (((end-start)/(2*duration))*((sample/sample_rate)**2))))
   
    frames = np.array(list(map(sweep_func, sweep)), dtype='f')

    return frames


# exponential sine function referenced from https://www.recordingblogs.com/wiki/sine-sweep
def exp_sweep(start, end, duration, sample_rate=sample_rate, st_amp=0.75, end_amp=0.75):
    '''
    Generate exponential sine chirp, with increasing or decreasing amplitude over time
    as frequency increases.
    :start: starting frequency (Hz)
    :end: ending frequency(Hz)
    :sample_rate: samples per second, default=48000
    :st_amp: starting amplitude, between 0 (no amplitude) and 1 (maximum amplitude), default=0.85
    :end_amp: ending amplitude, between 0 (no amplitude) and 1 (maximum amplitude), default=0.85
    Returns a numpy array of normalized floating-point frames.
    '''
    sweep_len = sample_rate * duration
    freq_ratio = end / start
    k = np.power(freq_ratio, 1/sweep_len)
    amp_array = np.linspace(st_amp, end_amp, num=sweep_len, endpoint=True)
    sweep = np.linspace(0, sweep_len, num=sweep_len, endpoint=False)

    def sweep_func(sample):
        return amp_array[int(sample)] * np.sin(two_pi * start * duration * (np.power(k, sample) - 1) / np.log(freq_ratio)) 

    sweep = np.array(list(map(sweep_func, sweep)), dtype='f')
    
    return sweep
