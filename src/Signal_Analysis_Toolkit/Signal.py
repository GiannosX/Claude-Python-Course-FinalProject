import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"

class Signal:  # Parent class 
    def __init__(self, duration: int=10, sample_rate: int=100, amplitude: int = 1, frequency: int = 1, phase: int = 0, noise: float=0):
        self.duration = duration 
        self.sample_rate = sample_rate
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.noise = noise

    def generate(self): # returns the signal array (NumPy format)
        pass

    @property # Property that gives the time array for plotting
    def samples(self): 
        return np.linspace(0,self.duration, self.sample_rate*self.duration + 1)

    def noisy(self, noise=0.5) -> Signal: 
        """
        returns an Object Signal that has noise and the generate function detects
        """
        return type(self)(self.duration, self.sample_rate, self.amplitude, self.frequency,self.phase, noise)

    def plot_signal(self): 
        t = self.samples
        fig ,ax = plt.subplots(figsize = (16,9))
        ax.plot(t, self.generate())
        ax.set_ylabel("Amplitude")
        ax.set_xlabel("Time")
        ax.grid(True)
        return ax

    def save_signal(self, tag:str=""): 
        df = pd.DataFrame({"time": self.samples, 
                           "amplitude_data": self.generate(), 
                           "type": type(self).__name__, 
                           "duration": self.duration, 
                           "sample_rate": self.sample_rate, 
                           "amplitude": self.amplitude, 
                           "frequency": self.frequency, 
                           "phase": self.phase, 
                           "noise": self.noise} )
        df.to_csv(DATA_DIR/ f"data_{tag}.csv", index=False)

def load_signal(filename: str): 
    df = pd.read_csv(DATA_DIR/filename)
    class_name = df["type"].iloc[0]
    #Dynamic subclass lookup
    subclasses = {cls.__name__: cls for cls in [Signal] + Signal.__subclasses__()}
    cls = subclasses.get(class_name, Signal)

    signal = cls(df["duration"].iloc[0], 
                 df["sample_rate"].iloc[0], 
                 df["amplitude"].iloc[0], 
                 df["frequency"].iloc[0], 
                 df["phase"].iloc[0], 
                 df["noise"].iloc[0])        
    # signal.samples = np.array(df["time"])
    signal.data = df["amplitude_data"].to_numpy()
    return signal

        

class SineSignal(Signal): 
    def __init__(self, duration: int, sample_rate: int, amplitude: int = 1, frequency: int = 1, phase: int = 0, noise: float=0):
        super().__init__(duration, sample_rate, amplitude, frequency, phase, noise)

    def generate(self): 
        if not hasattr(self, 'data'):
            x = self.samples
            self.data = self.amplitude*np.sin(x*self.frequency*2*np.pi + self.phase) + self.noise*self.amplitude*np.random.normal(0,1,size=len(self.samples)) # adds noise if its non zero
        return self.data

    def plot_signal(self): 
        ax = super().plot_signal()
        ax.set_title("Sinusoidal Signal")
        plt.show()

class SquareSignal(Signal): 
    def __init__(self, duration: int, sample_rate: int, amplitude: int = 1, frequency: int = 1, phase: int = 0, noise: float=0): 
        super().__init__(duration, sample_rate, amplitude, frequency, phase, noise)

    def generate(self): 
        if not hasattr(self, 'data'):
            x = self.samples
            period = 1/self.frequency
            square = np.where(x%period<period/2, self.amplitude, -self.amplitude)
            self.data = square + self.noise*self.amplitude*np.random.normal(0,1,size=len(self.samples)) # adds noise if its non zero
        return self.data

    def plot_signal(self): 
            ax = super().plot_signal()
            ax.set_title("Square Signal")
            plt.show()

