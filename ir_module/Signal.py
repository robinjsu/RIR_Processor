from distutils.log import error
import scipy.signal as signal
import math
from . import avg_signal as avg, convolve, default, gen_sine as gs, graph, impulse_response as ir


class Signal:
    def __init__(self, signal, sps=default.sample_rate, channels=default.channels, width=default.sample_width):
        '''
        Initialize an instance of the Signal class. Includes parameters pertaining to the sampling rate and format of the data.
        '''
        self._sample_rate = sps
        self._channels = channels
        self._sample_width = width
        self._signal = signal


    def get_state(self):
        '''
        Returns the sample rate, channel count, and sample size (in bytes).
        '''
        return self._sample_rate, self._channels, self._sample_width


    def get_sps(self):
        '''
        Returns the sampling rate (in Hz) of the signal.
        '''
        return self._sample_rate
    

    def get_signal(self):
        '''
        Returns the signal as a numpy array of floating-point values.
        '''
        return self._signal
    

    def set_state(self, signal, sps, channels, width):
        '''
        Set or change the base parameters of the Signal instance.
        '''
        self._sample_rate = sps
        self._channels = channels
        self._width = width
        self._signal = signal


    def set_signal(self, samples):
        '''
        Set or change the signal within the Signal instance.
        '''
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
        Returns a Signal instance containing the transformed signal
        '''
        assert self._sample_rate == impulse_response.get_sps(), f'impulse_response and signal sampling rates must match: Signal: {self.get_sps()}; Impulse Response: {impulse_response.get_sps()}'
        convolved = convolve.convolve_audio(self._signal, impulse_response.get_signal())

        return Signal(convolved, self._sample_rate, self._channels, self._sample_width)


    def deconvolve(self, input_signal):
        '''
        Extracts the impulse response from this Signal instance, which is assumed to be a recording of input_signal.
        Signal and input_signal must have matching sampling rates
        :input_signal: a Signal instance, with original input signal from which this Signal instance was generated.
        Returns a Signal instance representing the extracted impulse response
        '''
        assert self._sample_rate == input_signal.get_sps(), f'input signal sampling rate must match Signal instance'
        deconv = ir.deconvolve_invfilt(self._signal, input_signal.get_signal(), mode='freq')

        return Signal(deconv, self._sample_rate, self._channels, self._sample_width)


def average_signal(directory, num_frames):
    '''
    See documentation in avg_signal.py for more information.
    :directory: (string)
    :num_frames: (int)
    Returns a numpy array of floating-point values.
    '''
    return avg.xcorr_and_avg(directory, num_frames)


def generate_sine(freq=440, amp=.75, duration=1, start=440, end=440, start_amp=0.75, end_amp=0.75, sr=default.sample_rate, mode='lin'):
    '''
    Generate a sine wave or sweep of given duration.
    :freq: (int) frequency of standing sine wave
    :amp: (int) amplitude of a standing sine wave
    :duration: (int) duration of signal in seconds.
    :start: (int) if generating a sine sweep, the starting frequency
    :end: (int) if generating a sine sweep, the ending frequency
    :start_amp: (float) if generating a sine sweep, the starting amplitude. Between 0 and 1.
    :end_amp: (float) if generating a sine sweep, the ending amplitude. Between 0 and 1.
    :sr: (int) sampling rate (in Hz)
    :mode: ['sine', 'lin', 'exp'] Function mode. 'sine' will generate a sine wave of constant frequency. 'lin' and 'exp' will generate a sine sweep, of linear or exponential frequency growth, respectively. 
    Returns a numpy array of floating-point samples.
    '''
    samples = None
    if mode == 'sine':
        samples = gs.sine_wave(freq, duration, sample_rate=sr, amp=amp)
    elif mode == 'lin':
        samples = gs.lin_sweep(start, end, duration, sample_rate=sr, st_amp=start_amp, end_amp=end_amp)
    elif mode == 'exp':
        samples = gs.exp_sweep(start, end, duration, sample_rate=sr, st_amp=start_amp, end_amp=end_amp)
    
    return samples


def plot_fft(signal, save=False, fname=''):
    '''
    A utility function to plot the fft of the Signal instance. Option to save graph to given file.
    '''
    graph.graph_stft(signal, save=save, fname=fname)