### Winter 2022 Audio DSP Project

Independent Study
Winter 2022 at Portland State University

Robin Su, Masters in Computer Science (2022)
Advisor: by Bart Massey

The goal of this project was to implement various functions for processing recorded single impulses and digital sine sweeps, 
in order to generate an accurate room impulse response. 
The result is a small Python library to facilitate impulse response processing.

Attempts were made to record both single, short impulses (by clapping two pieces of wood together) and an exponential sine sweep that covered a large range of frequencies. An initial attempt was also made to generate what is essentially a Delta function, but the actual generated sound did not have enough power to properly generate a room response. For the sine sweeps, the exponential sweep, rather than the linear one, was most effective. 

### Module Functionality:
As mentioned above, the goal of this module is to package the processing signals to more easily extract useable room impulse responses from recorded samples.

To this effect, this module contains the following sub-modules:
* [`Signal.py`](./ir_module/Signal.py) definition and implementation of the Signal class, for easier handling of a discrete, digital signal. A class instance is initialized with key information about the original WAVE file parameters, including sampling rate, sample width, channels (mono, stereo, etc.), and more in order to facilitate the translation back to WAVE file format when writing the signal to a file (see all parameters in the Python [wave module](https://docs.python.org/3/library/wave.html) for in-depth information)
* [`wav_util.py`](./ir_module/wav_util.py) utility functions to manage WAVE files, so that signals can be handled as numpy arrays consisting of floating-point values. Includes functions that read/write to/from 16-bit and 24-bit WAVE files.
* [`graph.py`](./ir_module/graph.py) output a graph of the signal short-time Fourier transform (STFT), to help with visualizing the frequency content of a signal.
* [`avg_signal.py`](./ir_module/avg_signal.py) for repeated recorded signals that require averaging (typically to increase signal-to-noise ratio).
* [`convolve.py`](./ir_module/convolve.py) given an audio recording and an impulse response, the function convolves the audio recording to apply the room effects modeled by the impulse response function.
* [`impulse_reseponse.py`](./ir_module/impulse_response.py) extract the room impulse response of a recorded signal, given its original input signal
* [`default.py`](./ir_module/default.py) useful default constants that are frequently used throughout the module. can be overridden via keyword arguments where necessary.


#### Module Dependencies:
```pyaudio numpy scipy matplotlib wave```


### TODO LIST: 
* [X] make varying amplitude a CL arg? add option in linear sweep for varying amplitude (in `generate_sine.py`)
* [X] flesh out README - add some of the math functions and explanations
* [X] add a demo directory with samples for ppl to try out - add some more random midi files - can also give examples in README
* [X] add license to package requirements if I'm making this a Python Library
* [ ] test cross-correlation/shift functions

### References
A. Farina. “Simultaneous measurement of impulse response and distortion with a Swept-Sine technique”. 108th AES Convention. Paris, France. February 18-22, 2000.

A. Kamenov. "Sine sweep". RecordingBlogs - Wiki. (Publish Date Unavailable) \[Online\]. Available: https://www.recordingblogs.com/wiki/sine-sweep.