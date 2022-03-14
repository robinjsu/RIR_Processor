import numpy as np
from scipy import signal


def deconvolve_invfilt(output, input, mode='freq'):
    '''
    Deconvolve output signal using inverse filter convolution technique
    :output: output signal, usually the recorded signal
    :input: input signal, usually the original sine sweep
    Returns a floating-point numpy array of the impulse response.
    '''
    # create inverse filter
    input = np.array(input[::-1], dtype='f')
    # convolve with output signal
    m = 'fft' if mode == 'freq' else 'direct'
    conv = signal.convolve(output, input, mode='full', method=f'{m}')
    # normalize
    conv = (conv / conv[np.argmax(conv)])

    return conv

