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

"""Uncomment to switch between training and performance"""
#h5f = h5py.File(path + '/rstdp_performance_data.h5', 'r')
h5f = h5py.File(path + '/rstdp_training_data.h5', 'r')

"""Uncomment to print testing distance"""
#distance = np.array(h5f['distance_i'], dtype = float)
#print(max(distance))

steps = np.array(h5f['steps_i'], dtype = float)
rewards = np.array(h5f['reward_i'], dtype = float)

# data = [w_l, w_r]
print(max(steps))
fig = plt.figure(figsize=(20, 24))

ax1 = plt.subplot(313)
ax1.set_xlabel('Simulation Time [1 step = 50 ms]')
ax1.set_ylabel('Reward')
ax1.set_xlim(0, len(steps))
plt.grid(linestyle=':')
plt.plot(rewards)

fig.tight_layout()
plt.show()
