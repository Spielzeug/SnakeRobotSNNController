#!/usr/bin/env python

import numpy as np
from network import *
from environment import *
from parameters import *
import h5py

snn = SpikingNeuralNetwork()
env = VrepEnvironment()

path = "./data"
h5f = h5py.File(path+'/data_Am1.h5', 'r')
w_l = np.array(h5f['w_l'], dtype=float)[300-1]
w_r = np.array(h5f['w_r'], dtype=float)[300-1]
snn.set_weights(w_l,w_r)

distance = []
position = []

m = 0
s,r = env.reset()
for i in range(50000):
	n_l, n_r, w_l, w_r = snn.simulate(s,r)
	s,d,p,r,t,n,o = env.step(n_l, n_r)
	if p < 0.49:
		break
	distance.append(d)
	position.append(p)

h5f = h5py.File('./data/rstdp_data.h5', 'w')
h5f.create_dataset('distance', data=distance)
h5f.create_dataset('position', data=position)
h5f.close()