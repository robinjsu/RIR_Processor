import numpy as np
import scipy.signal as signal



def convolve_audio(source, impulse):
    '''
    Convolve source signal with impulse response (i.e. to add reverb effects to a dry audio file)
    :source: (array) input audio signal
    :impulse: (array) impulse response 
    Returns the convolved audio
    '''
    assert source[np.argmax(source)] <= 1.0 and source[np.argmin(source)] >= -1.0, f'ir samples not within bounds: {source[np.argmin(source)], source[np.argmax(source)]}'
    assert impulse[np.argmax(impulse)] <= 1.0 and impulse[np.argmin(impulse)] >= -1.0, f'ir samples not within bounds {impulse[np.argmin(impulse)], impulse[np.argmax(impulse)]}'

    zeros = np.zeros(len(impulse))
    padded_src = np.append(zeros, source)
    padded_src = np.append(padded_src, zeros)
    convolved = signal.convolve(padded_src, impulse, mode='full', method='auto')
    # normalize
    max_val = np.ceil(convolved[np.argmax(convolved)])
    scaled_conv = convolved * 0.75
   
    return scaled_conv[len(impulse):len(impulse)+len(source)]


# adapted from https://github.com/pdx-cs-sound/hw-resample/blob/master/filtercoeffs.py - Bart Massey
def lp_filter(source, nyquist_f):
    '''
    A simple low-pass filter.
    :source: the source signal to filter
    :nyquist_f: cutoff frequency value (typically the Nyquist frequency) 
    Returns a numpy array of floating-point values of the filtered signal.
    '''
    cutoff = nyquist_f * 0.45
    numtaps, beta = signal.kaiserord(60, 0.05)
    lpfilter = signal.firwin(numtaps, cutoff, window=('kaiser', beta), scale=True, fs=nyquist_f)
    filtered = signal.convolve(source, lpfilter, mode='full', method='auto')
    return filtered[:len(source)]