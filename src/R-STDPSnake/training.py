import numpy as np
import networkARMSTDP as arm
import networkMRMSTDP as mrm
import networkARMSTDPN as armn
from environment import*
from parameters import *
import h5py

"""Change between arm and mrm to train with additive and multiplicative scheme respectively"""

mrmSnn = arm.SpikingNeuralNetwork()
env = VrepEnvironment()
state = np.zeros((20*2,resolution[0],resolution[1]),dtype=int)
weights_r = []
weights_l = []
weights_i = []
episode_i = []
reward_i = []
steps_i = []

trained_weights_r = []
trained_weights_l = []
path = "./data"

m = 0
s,r,rc, areaLeft, areaRight = env.reset()
for i in range(15000):
    n_l, n_r, w_l, w_r = mrmSnn.simulate(s,r, rc, areaLeft, areaRight, False)
    s,r,rc,t,n, simStopped, distance, areaLeft, areaRight = env.step(n_l, n_r)
    
    if simStopped:
        trained_weights_l.append(w_l)
        trained_weights_r.append(w_r)
        episode_i.append(i)
        break
    if i % 100 == 0:
        weights_l.append(w_l)
        weights_r.append(w_r)
        weights_i.append(i)
        reward_i.append(r)
        steps_i.append(n)
    if t:
        episode_i.append(i)

h5f = h5py.File(path+'/rstdp_training_data.h5', 'w')
h5f.create_dataset('w_l', data=weights_l)
h5f.create_dataset('w_r', data=weights_r)
h5f.create_dataset('w_i', data=weights_i)
h5f.create_dataset('e_i', data=episode_i)
h5f.create_dataset('reward_i', data=reward_i)
h5f.create_dataset('steps_i', data=steps_i)
h5f.close()

h5f = h5py.File(path+'/rstdp_testing_data.h5', 'w')
h5f.create_dataset('w_l', data=trained_weights_l)
h5f.create_dataset('w_r', data=trained_weights_r)
