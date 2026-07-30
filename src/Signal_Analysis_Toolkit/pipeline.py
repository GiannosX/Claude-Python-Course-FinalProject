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