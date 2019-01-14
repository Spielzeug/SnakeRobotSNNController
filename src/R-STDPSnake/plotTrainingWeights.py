'''
@author: clamesc
'''

import numpy as np
import h5py
from environment import *
import matplotlib.pyplot as plt
from matplotlib import gridspec

# R-STDP training progress

env = VrepEnvironment()

path = "./data"
h5f = h5py.File(path + '/rstdp_training_data.h5', 'r')


w_l = np.array(h5f['w_l'], dtype=float)
w_r = np.array(h5f['w_r'], dtype=float)
w_i = np.array(h5f['w_i'], dtype=float)
e_i = np.array(h5f['e_i'], dtype=float)

xlim = max(e_i) 

fig = plt.figure(figsize=(7,8))
gs = gridspec.GridSpec(2, 1, height_ratios=[2, 2]) 

ax3 = plt.subplot(gs[0])
ax3.set_ylabel('Weight', position=(0.,0.))
ax3.set_xlim((0,xlim))
ax3.set_ylim((180,220))
ax3.set_xticklabels([])
ax3.text(1000, 2100, 'Left Motor', color='0.4')
ax3.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)
for i in range(w_l.shape[1]):
    for j in range(w_l.shape[2]):
        plt.plot(w_i, w_l[:,i,j])

ax4 = plt.subplot(gs[1], sharey=ax3)
ax4.set_xlim((0,xlim))
ax4.set_ylim((180,220))
ax4.text(1000, 2100, 'Right Motor', color='0.4')
ax4.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)
for i in range(w_r.shape[1]):
    for j in range(w_r.shape[2]):
        plt.plot(w_i, w_r[:,i,j])
ax4.set_xlabel('Simulation Time [1 step = 50 ms]')


fig.tight_layout()
plt.subplots_adjust(wspace=0., hspace=0.)
plt.show()