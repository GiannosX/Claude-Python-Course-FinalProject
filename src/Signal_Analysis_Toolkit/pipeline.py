import numpy as np 
import matplotlib.pyplot as plt 
from .signal import Signal, SineSignal, SquareSignal

class SignalPipeline: 
    """
    class that takes a Signal and applies a list of processing steps: 
    for example: 
    1. Plots the signal
    2. Plots the signal in frequency domain 
    3. prints the mean, std, rms, 
    """
    def __init__(self): 
        self.steps = []

    def add_step(self, func): 
        self.steps.append(func)
        return self

    def run(self, signal): 
        result = signal
        for step in self.steps: 
            result = step(result)
        return result

def remove_dc(signal): 
    return signal - np.mean(signal)

def smooth(signal, window=3, normal=False): 
    if normal:
        x = np.arange(window) - (window-1)/2
        sigma = np.sqrt(window)/1.2
        kernel = np.exp(-(x**2)/(2*sigma**2))
        kernel /= kernel.sum()      #Normalize the kernel
        smoothed = np.convolve(signal, kernel, mode='same')
    else: 
        kernel = np.ones(window) / window
        smoothed = np.convolve(signal, kernel, mode='same')
    return smoothed    

def find_dominant_frequency(signal, sample_rate):
    fft_signal = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), d=1/sample_rate)
    half = len(signal)//2
    positive_freqs = freqs[:half]
    magnitude = np.abs(fft_signal[:half])
    peak_index = np.argmax(magnitude)
    return positive_freqs[peak_index]

def min_max_normalize(signal):
    return (signal - signal.min())/(signal.max()-signal.min())

def z_score_normalize(signal):
    return (signal - signal.mean())/signal.std()

def clip_outliers(signal, n_std=3):
    mean, std = signal.mean(), signal.std()
    return np.clip(signal, mean-n_std*std, mean + n_std*std)

def lowpass_filter(signal, sample_rate, cutoff):
    fft_vals = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), d=1/sample_rate)
    fft_vals[np.abs(freqs) > cutoff] = 0
    return np.fft.ifft(fft_vals).real

def highpass_filter(signal, sample_rate, cutoff): 
    fft_vals = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), d=1/sample_rate)
    fft_vals[np.abs(freqs) < cutoff] = 0
    return np.fft.ifft(fft_vals).real

def bandpass_filter(signal, sample_rate, low, high): 
    fft_vals = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), d=1/sample_rate)
    fft_vals[np.abs(freqs) < low] = 0
    fft_vals[np.abs(freqs) > high] = 0
    return np.fft.ifft(fft_vals).real