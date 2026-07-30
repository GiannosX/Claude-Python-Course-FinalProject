import numpy as np
import matplotlib.pyplot as plt
from .signal import Signal, SineSignal, SquareSignal, load_signal
from .pipeline import SignalPipeline, remove_dc, smooth
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"

sine = SineSignal(5, 100,amplitude=10, frequency=1)
sine_noisy = sine.noisy(0.5)
square = SquareSignal(5, 100, amplitude=5, frequency=2)
square_noisy = square.noisy(0.4)



fig, ax = plt.subplots(2,1,figsize=(15,12))
ax[0].plot(np.linspace(0,100,len(sine_noisy.generate())), sine_noisy.generate())
ax[0].plot(np.linspace(0,100,len(sine.generate())), sine.generate(), color="g", ls="--")
ax[0].grid(True)
ax[0].set_title("Noisy Signal")
line, = ax[1].plot(np.linspace(0,100,len(smooth(sine_noisy.generate()))), smooth(sine_noisy.generate(), window=1))
ax[1].plot(np.linspace(0,100,len(sine.generate())), sine.generate(), color="g", ls=":")
ax[1].grid(True)
for j in [0,1]:
    for i in range(1,80):
        ax[1].set_title(f"Smoothed signal, window={i}")
        line.set_ydata( smooth(sine_noisy.generate(), window=i, normal=j))
        plt.savefig(DATA_DIR/"figure.png")
        plt.pause(0.10) #Pause before the next figure
