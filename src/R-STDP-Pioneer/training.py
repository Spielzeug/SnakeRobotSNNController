#!/usr/bin/env python

import numpy as np
from network import *
from environment import *
from parameters import *
import h5py

snn = SpikingNeuralNetwork()
env = VrepEnvironment()
state = np.zeros((20*2,resolution[0],resolution[1]),dtype=int)
weights_r = []
weights_l = []
weights_i = []
episode_position_o = []
episode_i_o = []
episode_position_i = []
episode_i_i = []
path = "./data"

m = 0
s,r = env.reset()
for i in range(100000):
	n_l, n_r, w_l, w_r = snn.simulate(s,r)
	s,d,p,r,t,n,o = env.step(n_l, n_r)
	if i % 100 == 0:
		weights_l.append(w_l)
		weights_r.append(w_r)
		weights_i.append(i)
	if t:
		if o:
			episode_position_o.append(p)
			episode_i_o.append(i)
		else:
			episode_position_i.append(p)
			episode_i_i.append(i)
		print i, p

h5f = h5py.File(path+'/data_sc3.h5', 'w')
h5f.create_dataset('w_l', data=weights_l)
h5f.create_dataset('w_r', data=weights_r)
h5f.create_dataset('w_i', data=weights_i)
h5f.create_dataset('e_o', data=episode_position_o)
h5f.create_dataset('e_i_o', data=episode_i_o)
h5f.create_dataset('e_i', data=episode_position_i)
h5f.create_dataset('e_i_i', data=episode_i_i)
h5f.close()