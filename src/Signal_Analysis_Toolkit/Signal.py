import numpy as np
import matplotlib.pyplot as plt 

class Signal: 
    def __init__(self, duration: float, sample_rate: int, amplitude: int = 1, frequency: int = 1, phase: int = 0):
        self.duration = duration 
        self.sample_rate = sample_rate
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase

    def generate(self): 
        pass

    @property 
    def samples(self): 
        return np.linspace(0,self.duration, self.sample_rate*self.duration)


class SineSignal(Signal): 
    def __init__(self, duration: int, sample_rate: int, amplitude: int = 1, frequency: int = 1, phase: int = 0):
        super().__init__(duration, sample_rate, amplitude, frequency, phase)

    def generate(self): 
        x = self.samples
        return self.amplitude*np.sin(x*self.frequency*2*np.pi + self.phase)

class SquareSignal(Signal): 
    def __init__(self, duration: int, sample_rate: int, amplitude: int = 1, frequency: int = 1, phase: int = 0): 
        super().__init__(duration, sample_rate, amplitude, frequency, phase)

    def generate(self): 
        x = self.samples
        square = [self.amplitude for _ in x if _<_%self.frequency else -self.amplitude]


y = SquareSignal(5, 100, frequency=2)
t = y.samples

fig ,ax = plt.subplots(figsize = (16,9))
ax.plot(t, y.generate())
ax.set_title("Sinusoidal Signal")
ax.grid(True)
plt.show()


