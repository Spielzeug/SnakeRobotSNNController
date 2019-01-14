'''
@author: Dmitry Kochikiyan
'''

import numpy as np
import h5py
import parameters as P
import matplotlib.pyplot as plt
from matplotlib import gridspec

# Load the training data
path = "./data"
h5f = h5py.File(path + '/rstdp_training_data.h5', 'r')

w_l = np.array(h5f['w_l'], dtype=float)
w_r = np.array(h5f['w_r'], dtype=float)
w_i = np.array(h5f['w_i'], dtype=float)
steps = np.array(h5f['steps_i'], dtype = float)
rewards = np.array(h5f['reward_i'], dtype = float)

ylabels = ['Weights Left', 'Weights Right']

data = [w_l, w_r]

fig = plt.figure(figsize=(20, 24))

ax1 = plt.subplot(313)
ax1.set_xlabel('Simulation Time [1 step = 50 ms]')
ax1.set_ylabel('Reward')
ax1.set_xlim(0, len(steps))
plt.grid(linestyle=':')
plt.plot(rewards)

fig.tight_layout()
plt.show()
