import numpy as np
import matplotlib.pyplot as plt 

class Signal:  # Parent class 
    def __init__(self, duration: int, sample_rate: int, amplitude: int = 1, frequency: int = 1, phase: int = 0, noise: float=0):
        self.duration = duration 
        self.sample_rate = sample_rate
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.noise = noise

    def generate(self): # returns the signal array 
        pass

    @property # Property that gives the time array for plotting
    def samples(self): 
        return np.linspace(0,self.duration, self.sample_rate*self.duration)

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
        

class SineSignal(Signal): 
    def __init__(self, duration: int, sample_rate: int, amplitude: int = 1, frequency: int = 1, phase: int = 0, noise: float=0):
        super().__init__(duration, sample_rate, amplitude, frequency, phase, noise)

    def generate(self): 
        x = self.samples
        return self.amplitude*np.sin(x*self.frequency*2*np.pi + self.phase) + self.noise*self.amplitude*np.random.normal(0,1,size=len(self.samples)) # adds noise if its non zero

    def plot_signal(self): 
        ax = super().plot_signal()
        ax.set_title("Sinusoidal Signal")
        plt.show()

class SquareSignal(Signal): 
    def __init__(self, duration: int, sample_rate: int, amplitude: int = 1, frequency: int = 1, phase: int = 0, noise: float=0): 
        super().__init__(duration, sample_rate, amplitude, frequency, phase, noise)

    def generate(self): 
        x = self.samples
        square = [self.amplitude if i%(1/self.frequency)<(1/self.frequency)/2 else -self.amplitude for i in x]
        return np.array(square) + self.noise*self.amplitude*np.random.normal(0,1,size=len(self.samples)) # adds noise if its non zero

    def plot_signal(self): 
            ax = super().plot_signal()
            ax.set_title("Square Signal")
            plt.show()


y = SineSignal(5, 100,amplitude=2, frequency=1)

y_noisy = y.noisy(0.3)
y_noisy.plot_signal()


