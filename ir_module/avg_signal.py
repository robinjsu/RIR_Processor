import os, glob
import numpy as np
from scipy import signal

import wav_util, default

def retrieve_wave_files(directory, num_frames):
    '''
    Reads in a batch of wave files within a single specified directory.
    :directory: file directory containing desired files
    :num_frames: for simplicity, all files will be constrained in length (number of frames)
    Returns an numpy ndarray of samples
    '''
    samples_array = []
    sample_rate = None
    sample_width = None
    file_dir = os.path.join(f'{directory}', '*.wav')
    files = glob.glob(file_dir)
    for file in files:
        params, samples = wav_util.read_wave_nbit(file)
        assert len(samples) >= num_frames, f'all files must be at least of length {num_frames}. {file} is too short: {len(samples)} frames'
        if sample_rate is None:
            sample_rate = params.framerate
        assert params.framerate == sample_rate, f'{file}: sampling rate mismatch. all files must be at same sampling rate.' 
        if sample_width is None:
            sample_width = params.sampwidth
        assert params.sampwidth == sample_width, f'{file}: sample/frame width mismatch. all  files must be at same frame width.'
        samples_array = np.append(samples_array, samples[:num_frames])
    samples_array = samples_array.reshape(len(files), num_frames)

    return samples_array


def upsample(samples_to_upsamp, upsamp_factor=default.upsample_rate):
    '''
    Upsamples the original files by the given factor
    :samples_to_upsamp: original array of samples
    :upsamp_factor: factor by which to upsample
    '''
    upsamples_arr = []
    samples = len(samples_to_upsamp[0])
    upsamples = samples * upsamp_factor
    tests = len(samples_to_upsamp)
    for i in range(tests):
        upsampled = signal.resample(samples_to_upsamp[i], len(samples_to_upsamp[i])*upsamp_factor)
        upsamples_arr = np.append(upsamples_arr, upsampled)

    upsamples_arr = upsamples_arr.reshape(tests,upsamples)
    return upsamples_arr


# https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.correlation_lags.html
def xcorrelate(samples_x, samples_y):
    '''
    Calculate the cross-correlation to determine relative time shift of samples_x and samples_y.
    :samples_x: First array of discrete signal frames
    :samples_y: Second array of discrete signal frames
    Returns: lag - an integer representing the lag value. 
    If lag is positive, samples_y leads samples_x if lag is negative, samples_y lags samples_x. 
    If lag is 0, samples_x and samples_y are already maximally correlated.
    '''
    correlation = np.correlate(samples_x, samples_y, mode='same')
    lags = signal.correlation_lags(samples_x.size, samples_y.size, mode='same')
    lag = lags[np.argmax(correlation)]
    return lag


def shift_signal(samples, lag):
    '''
    Shift signal with (positive or negative) lag. Pads with zeros to maintain same signal length.
    :samples: signal array
    :lag: (int) amount of shift
    '''
    if lag == 0:
        return samples.copy() 

    zeros = np.zeros(np.abs(lag))
    new_samples = samples.copy()
    if lag > 0:
        new_samples = np.append(zeros, new_samples)
        new_samples = new_samples[:lag*-1]
    else:
        new_samples = np.append(new_samples, zeros)
        new_samples = new_samples[np.abs(lag):]
    
    assert len(samples) == len(new_samples), f'shifted samples differ in length from original - samples: {len(samples)}; new_samples: {len(new_samples)} '

    return new_samples


def xcorr_and_avg(source_samples_dir, nframes):
    source_samples_arr = retrieve_wave_files(source_samples_dir, nframes)

    # upsample for higher accuracy cross-correlation
    upsampled_arr = upsample(source_samples_arr)
    avg_signal = upsampled_arr[0]
    for s in upsampled_arr:
        lag = xcorrelate(avg_signal, s)
        shifted = shift_signal(s, lag)
        avg_signal = np.average(np.array([avg_signal, shifted]), axis=0)
    
    # downsample
    avg_signal = signal.decimate(avg_signal, 2, ftype='fir', zero_phase=True)
    
    return avg_signal
    