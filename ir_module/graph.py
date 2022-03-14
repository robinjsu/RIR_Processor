import numpy as np
from time import time
import matplotlib.pyplot as plt
from scipy import signal
from .default import *

def graph_stft(sig, save=False, fname='', fft_sz=fft_sz):
    '''
    Calculate stft of signal and plot graph of magnitude spectrum
    :samples_arr: array of signal samples in 16-bit integer format
    '''
    f_out,t_out,stft = signal.stft(sig, nperseg=2048, nfft=fft_sz)
    plt.pcolormesh(t_out, f_out, np.abs(stft), shading='auto')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()
    if save == True:
        filename = fname if fname != '' else f'stft_graph_{time()}'
        plt.savefig(f'{filename}')

