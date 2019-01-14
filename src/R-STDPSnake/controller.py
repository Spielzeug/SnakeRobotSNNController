import numpy as np
import networkARMSTDP as arm
import networkMRMSTDP as mrm
from environment import*
from parameters import *
import h5py
#import vrep as vrep
#import vrepConst


"""Change between arm and mrm to test with additive and multiplicative scheme respectively"""

path = "./data"

# Read network weights
h5f = h5py.File(path + '/rstdp_testing_data.h5', 'r')
w_l = np.array(h5f['w_l'], dtype=float)[-1]
w_r = np.array(h5f['w_r'], dtype=float)[-1]
# Set network weights

distance = []
reward_i = []

m = 0

completed = 0
failed = 0
#vrep.simxFinish(-1)
#clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5)

#vrep.simxSynchronous(clientID,True)

for j in range(5):
    snn = mrm.SpikingNeuralNetwork()
    snn.set_weights(w_l,w_r)
    
    env = VrepEnvironment()
    state = np.zeros((20*2,resolution[0],resolution[1]),dtype=int)
    
    s,r,rc, areaLeft, areaRight = env.reset()
    simStopped = False
    t = False
    
    #e = vrep.simxStartSimulation(clientID,vrep.simx_opmode_blocking)
    
    for i in range(50000):

    # Simulate network for 50 ms
    # Get left and right output spikes, get weights
        n_l, n_r, w_l, w_r = snn.simulate(s,r, rc, areaLeft, areaRight, True)

    # Feed output spikes into steering wheel model
    # Get state, distance, position, reward, termination, step, lane
        s,r,rc,t,n, simStopped, d, areaLeft, areaRight = env.step(n_l, n_r)

    # Break episode if robot reaches starting position again
        if simStopped:
            completed += 1
            break
        elif t:
            failed +=1
            break
    # Store position, distance
        distance.append(d)
        reward_i.append(r)
    print ("completed: ", completed, "failed: ", failed)
    #vrep.simxStopSimulation(clientID, vrep.simx_opmode_blocking)
print ("completed: ", completed, "failed: ", failed)

h5f = h5py.File(path + '/rstdp_performance_data.h5', 'w')
h5f.create_dataset('distance', data=distance)
h5f.create_dataset('reward_i', data=reward_i)
h5f.close()