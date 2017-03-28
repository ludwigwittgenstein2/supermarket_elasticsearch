"""Produce custom labelling for a colorbar.

Contributed by Scott Sinclair
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from numpy.random import randn

# Make plot with vertical (default) colorbar
fig, ax = plt.subplots()

data = np.clip(randn(250, 250)*12, -10, 10)   # 250 by 250 array, values clipped to +/-10

cax = ax.imshow(data, interpolation='nearest', cmap=cm.ocean)
ax.set_title('Gaussian noise with vertical colorbar')

# Add colorbar, make sure to specify tick locations to match desired ticklabels
# cbar = fig.colorbar(cax, ticks=[-10, -8, -2,-1, 0, 0.5, 1, 2, 8, 10])
cbar = fig.colorbar(cax, ticks=[-10, -8, -2, -1, 0, 0.5, 1, 2, 8, 10])
cbar.ax.set_yticklabels(['dog', 'cat', 'sheep', 'cow',
                         'chicken', 'pig', 'rooster', '2', '8', '10'])  # vertically oriented colorbar

plt.show()
