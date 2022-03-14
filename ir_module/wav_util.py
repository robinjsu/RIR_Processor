import numpy as np
import pyaudio
import struct, wave as w

'''
handle wav files
'''
def read_wave_16bit(wav_obj, params):
    '''
    Read 16-bit wave file and convert to a Python array
    Returns the array of floating-point values
    :wav_obj: wave object
    :params: wave object parameters
    '''
    assert params.sampwidth == 2, f'file is not in 16-bit format. actual: {params.sampwidth * 8} bit'
    assert params.nchannels == 1, f'file is not mono. actual: {params.nchannels} channels'

    frames = wav_obj.readframes(params.nframes)
    sample_array = struct.unpack(f'<{params.nframes}h', frames)
    samples = np.array(sample_array, 'f')
    samples = samples / (2**15)

    return samples

# written by Bart Massey
def read_wave_24bit(wave_obj, params):
    '''
    Read  24-bit wave file and convert to a Python array
    Returns the array of floating-point values
    :wav_obj: wave object
    :params: wave object parameters
    '''
    assert params.sampwidth == 3, "not 24-bit"
    assert params.nchannels == 1, "not mono"

    frames = wave_obj.readframes(params.nframes)
    frames = [
        frames[i] | (frames[i + 1] << 8) | (frames[i + 2] << 16)
        for i in range(0, params.nframes * 3, 3)
    ]
    # https://stackoverflow.com/a/32031543
    sign_bit = 0x800000
    sign_mask = sign_bit - 1
    def sign_extend(value):
        return (value & sign_mask) - (value & sign_bit)
    frames = [sign_extend(f) / sign_bit for f in frames]
    frames = np.array(frames, 'f')
    
    return frames

def read_wave_nbit(wavfile):
    '''
    Unpack wave file to a floating-point numpy array
    Return wave file parameters and frames 
    '''
    with w.open(wavfile, 'rb') as wav:
        params = wav.getparams()
        num_frames = wav.getnframes()

        frames = None
        if params.sampwidth == 2:
            frames = read_wave_16bit(wav, params)
        elif params.sampwidth == 3:
            frames = read_wave_24bit(wav, params)
        else:
            TypeError(f'{wavfile} is an unknown format: {params.sampwidth * 8} bit')
        
    if frames.any() > 1.0:
        frames = frames / frames[np.argmax(frames)]
    elif frames.any() < -1.0:
        frames = frames / (frames[np.argmin(frames)] * -1)

    return params, frames

def write_wav_file_16bit(file, frames, channels, samp_rate, sampwidth):
    '''
    Convert floating-point array of audio samples (frames) to a bytes object, 
    and write bytes out to wav file format
    :file: (str) name of file to write 
    :frames: floating-point numpy array of samples (currently handles mono-channel only)
    :channels: (int) number of channels 
    :samp_rate: (int) sampling rate in Hz
    :sampwidth: (int) bit-width of sample in bytes
    '''
    fbytes = samples_to_bytes_16bit(frames)
    wav = w.open(file, 'wb')
    wav.setnchannels(channels)
    wav.setsampwidth(sampwidth)
    wav.setframerate(samp_rate)
    wav.setnframes(samp_rate)
    wav.writeframes(fbytes)
    wav.close()


def play_wav_16bit(samples, samp_rate, channels, dtype):
    samples = samples_to_bytes_16bit(samples)
    py_audio = pyaudio.PyAudio()
    wav_stream = py_audio.open(
                    samp_rate, 
                    channels, 
                    dtype, 
                    output=True)

    wav_stream.write(samples)
    wav_stream.stop_stream()
    py_audio.close(wav_stream)
    py_audio.terminate()


def bytes_to_samples_16bit(data, frames):
    '''
    Unpack bytes to an array of 16-bit integers
    Returns the array of 16-bit integers
    :data: bytes or bytearray object
    :frames: (int) number of frames in the data
    '''
    sample_array = struct.unpack(f'<{frames}h', data)
    samples = np.array(sample_array, f'<i2')

    return samples

def samples_to_bytes_16bit(sample_array):
    '''
    Translate array of floating-point samples into a bytes object
    Returns the bytes
    :sample_array: array of samples
    :dtype: data type of the samples
    '''
    assert sample_array[np.argmax(sample_array)] < 1, f'input samples must be floating-point values between 0 and 1. type: {sample_array.dtype}; max value: {sample_array[np.argmax(sample_array)]}'
    samples_16bit = sample_array * (2**15)
    arr = np.array(samples_16bit, dtype='<i2')
    signal_bytes = arr.tobytes()

    return signal_bytes




