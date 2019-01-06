import numpy as np
import networkARMSTDP as arm
import networkMRMSTDP as mrm
from environment import*
from parameters import *
import h5py

mrmSnn = mrm.SpikingNeuralNetwork()
env = VrepEnvironment()
state = np.zeros((20*2,resolution[0],resolution[1]),dtype=int)
weights_r = []
weights_l = []
weights_i = []
episode_i = []
path = "./data"

m = 0
s,r,rc = env.reset()
for i in range(15000):
    n_l, n_r, w_l, w_r = mrmSnn.simulate(s,r, rc)
    s,r,rc,t,n = env.step(n_l, n_r)
    if i % 100 == 0:
        weights_l.append(w_l)
        weights_r.append(w_r)
        weights_i.append(i)
    if t:
        episode_i.append(i)

h5f = h5py.File(path+'/data.h5', 'w')
h5f.create_dataset('w_l', data=weights_l)
h5f.create_dataset('w_r', data=weights_r)
h5f.create_dataset('w_i', data=weights_i)
h5f.create_dataset('e_i', data=episode_i)
h5f.close()