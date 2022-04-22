### Winter 2022 Audio DSP Project

An Independent Study Project
Winter 2022 at Portland State University

Robin Su, Masters in Computer Science (2022)
Advised by Bart Massey

The goal of this project was to implement various functions for processing recorded single impulses and digital sine sweeps, 
in order to generate an accurate room impulse response. 
The result is a small Python library to facilitate impulse response processing.

-----
### Demo
#### Extracted Impulse Response:
![](./demo/impulse_responses/garage_impulse_isolated.wav)

### Module Functionality:
The goal of this module is to package the processing signals to more easily extract useable room impulse responses from recorded audio files. Deals primarily with 16-bit WAVE files, but also supports reading/writing 24-bit files.

To this effect, this module contains the following sub-modules:
* [`Signal.py`](./ir_module/Signal.py) definition and implementation of the Signal class, for easier handling of discrete, digital signals. A class instance is initialized with key signal parameters, including sampling rate, sample width, and number of channels (mono, stereo, etc.) in order to facilitate the translation between discrete samples and WAVE file format (more information in the documentation for the Python [wave module](https://docs.python.org/3/library/wave.html)).
* [`wav_util.py`](./ir_module/wav_util.py) utility functions to manage WAVE files, so that signals can be handled as numpy arrays consisting of floating-point values. Includes functions that read/write to/from 16-bit and 24-bit WAVE files.
* [`graph.py`](./ir_module/graph.py) output a graph of the signal short-time Fourier transform (STFT), to help with visualizing the frequency content of a signal.
* [`avg_signal.py`](./ir_module/avg_signal.py) takes a batch of repeated recorded audio signals, cross-correlates them, and performs an average over the batch (typically to increase signal-to-noise ratio).
* [`convolve.py`](./ir_module/convolve.py) given an audio recording and an impulse response, the function convolves the audio recording to apply the room effects modeled by the impulse response function.
* [`impulse_reseponse.py`](./ir_module/impulse_response.py) extract the room impulse response of a recorded signal, given the reference input signal
* [`default.py`](./ir_module/default.py) useful default constants that are frequently used throughout the module. Can be overridden via keyword arguments where necessary.

-----
### Module Dependencies:
```pyaudio numpy scipy matplotlib wave```

-----

An example of the intended functionality of this module is included in the files [`demo.py`](demo.py) and [`demo_reverb.py`](./demo_reverb.py). 

Sample wav files are included in the [demo](./demo/) directory:
 * [dry_audio](./demo/dry_audio/): dry audio recordings that can be convlved with the impulse responses to produce an track with "reverb".
 * [impulse_responses](./demo/impulse_responses/): the resulting impulse responses of three different microphone placements or spaces
 * [recorded_output](./demo/recorded_output/): recorded sweeps
 * [sweeps](./demo/sweeps/): example exponential sine sweeps used as input to generate a room response.

-----
### References (cited in the code where relevant)
A. Farina. “Simultaneous measurement of impulse response and distortion with a Swept-Sine technique”. 108th AES Convention. Paris, France. February 18-22, 2000.

A. Kamenov. "Sine sweep". RecordingBlogs - Wiki. (Publish Date Unavailable) \[Online\]. Available: https://www.recordingblogs.com/wiki/sine-sweep.

Wikipedia. "Chirp". https://en.wikipedia.org/wiki/Chirp. 