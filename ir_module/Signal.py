from distutils.log import error
import scipy.signal as signal
import math
from .default import *
from .graph import graph_stft
from .impulse_response import deconvolve_invfilt
import avg_signal as avg
import convolve as conv

# TODO: if resample is a downsample, should I include a a decimate(lp_filter func in convolve.py)?
# TODO: how to properly extract IR from the deconvolved result? where do I truncate the signal before the actual impulse?
# TODO: scale graphing function to have tighter bounds on the fft graph (how to scale Frequency (y axis?))

class Signal:
    def __init__(self, signal, sps=sample_rate, channels=channels, width=sample_width):
        self._sample_rate = sps
        self._channels = channels
        self._sample_width = width
        self._signal = signal


    def get_state(self):
        return self._sample_rate, self._channels, self._sample_width
    

    def get_sps(self):
        return self._sample_rate
    
    def get_signal(self):
        return self._signal
    
    def set_state(self, signal, sps, channels, width):
        self._sample_rate = sps
        self._channels = channels
        self._width = width
        self._signal = signal

    def set_signal(self, samples):
        self._signal = samples
    
    def copy(self):
        cp_rate, cp_chan, cp_width = self.get_state()
        cp_signal = self._signal
        copied = Signal(cp_rate, cp_chan, cp_width)
        copied.set_signal(cp_signal)

        return copied
    
    def resample(self, new_sps):
        '''
        Up- or down-sample signal to new_sps sampling rate
        :new_sps: New sampling rate, can be value greater or less than original sampling rate.
        Returns the new sampling upon successful resampling
        '''
        if self._sample_rate == new_sps:
            return new_sps

        signal_length = int(math.floor(len(self._signal) / self._sample_rate))
        old_sps = self._sample_rate
        self._sample_rate = new_sps
        resamp_factor = new_sps / self._sample_rate
        new_frames = int(len(self._sample_rate) * resamp_factor)
        resampled = signal.resample(self._signal, new_frames)
        self._signal = resampled
        
        if int(math.floor((self._signal / new_sps))) != signal_length:
            self._sample_rate = old_sps
            error(f'error in converting sampling rate from {old_sps}sps to {new_sps}sps')
        
        return new_sps
    

    def convolve(self, impulse_response):
        '''
        Assumes the Signal instance is a dry audio signal, convolve with given room impulse response to get a transformed signal.
        If Signal and impulse_response are not of same sampling rate, the impulse_response will be resampled to match the Signal
        :impulse_response: a Signal instance, containing a numpy array of floating-point values representing a room impulse response
        Returns a numpy array of floating-point values representing the transformed signal
        '''
        assert self._sample_rate == impulse_response.get_sps(), f'impulse_response and signal sampling rates must match: Signal: {self.get_sps()}; Impulse Response: {impulse_response.get_sps()}'
        convolved = conv.convolve_audio(self._signal, impulse_response.get_signal())
        return convolved


    def deconvolve(self, input_signal):
        '''
        Extracts the impulse response from this Signal instance, which is assumed to be a recording of input_signal.
        Signal and input_signal must have matching sampling rates
        :input_signal: a Signal instance, with original input signal from which this Signal instance was generated.
        Returns a numpy array of floating-point values representing the extracted impulse response
        '''
        assert self._sample_rate == input_signal.get_sps(), f'input signal sampling rate must match Signal instance'
        deconv = deconvolve_invfilt(self._signal, input_signal.get_signal(), mode='freq')
        return deconv


def average_signal(directory, file_base=''):
    pass


def generate_sine(start=440, end=440, start_amp=0.75, end_amp=0.75, duration=1, mode='lin'):
    pass


def plot_fft(signal, save=False, fname=''):
    '''
    A utility function to plot the fft of the Signal instance. Option to save graph to given file.
    '''
    graph_stft(signal, save=save, fname=fname)


    '''
    potential member functions:
    - convolve(given impulse response file)
    - generate sine(all the parameters)
    - deconvolve (return can be impulse response)
    - plot signal (either time or frequency domain)
    non member functions:
    - average signal from batch of files 
    '''