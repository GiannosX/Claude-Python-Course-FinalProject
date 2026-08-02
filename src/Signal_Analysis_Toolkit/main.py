import numpy as np
import matplotlib.pyplot as plt
from .signal import Signal, SineSignal, SquareSignal, load_signal
from .pipeline import SignalPipeline, remove_dc, smooth, find_dominant_frequency, min_max_normalize, z_score_normalize, lowpass_filter, highpass_filter, bandpass_filter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"

sine = SineSignal(5, 100,amplitude=10, frequency=1)
sine_noisy = sine.noisy(0.5)
square = SquareSignal(5, 100, amplitude=5, frequency=2)
square_noisy = square.noisy(0.4)

# pipleline = SignalPipeline()
# pipleline.add_step(lowpass_filter)
# pipleline.add_step(smooth)

processed = sine_noisy.generate()
processed = lowpass_filter(processed, cutoff=2)
processed = smooth(processed, window=20, normal=True)

fig, ax = plt.subplots(3,1,figsize=(14,10))
ax[0].plot(range(len(sine.generate())), sine.generate())
ax[0].set_title("Clean signal")
ax[0].grid(True)
ax[1].plot(range(len(sine_noisy.generate())), sine_noisy.generate())
ax[1].set_title("Noisy signal")
ax[1].grid(True)
ax[2].plot(range(len(processed)), processed)
ax[2].set_title("processed signal")
ax[2].grid(True)
plt.show()

# processed = square_noisy.generate()
# # processed = highpass_filter(processed, cutoff=2)
# processed = smooth(processed, window=3, normal=True)

# fig, ax = plt.subplots(3,1,figsize=(14,10))
# ax[0].plot(range(len(square.generate())), square.generate())
# ax[0].set_title("Clean signal")
# ax[0].grid(True)
# ax[1].plot(range(len(square_noisy.generate())), square_noisy.generate())
# ax[1].set_title("Noisy signal")
# ax[1].grid(True)
# ax[2].plot(range(len(processed)), processed)
# ax[2].set_title("processed signal")
# ax[2].grid(True)
# plt.show()