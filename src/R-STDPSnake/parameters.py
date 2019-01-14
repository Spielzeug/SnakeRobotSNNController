import numpy as np

dvs_resolution = [128,128]
crop_top = 0
crop_bottom = 16
resolution = [8,4]
time_resolution = 0.1
max_spikes = 15.0
max_poisson_freq = 300.0
sim_time = 50.0

observation_neurons_count = resolution[0] * resolution[1]
actions = {'turn_left' : 0, 'turn_right' : 1}
action_neurons_count = len(actions)

weight_seed = 0
noise_seed = [928]

#noise inputs to all state and actions neurons
noise_params = {'mean' : 0.0, 'std' : 100.}
#spike detector parameters 
sd_params = {"withtime" : True, "withgid" : True, 'to_file' : False, 'flush_after_simulate' : True, 'flush_records' : True}

#neuron parameters
neuronparams = { 'tau_m':20., 'V_th':-50., 'E_L':-60., 't_ref':2., 'V_reset':-60., 'C_m':200. }
#synapse parameters
#stdp_synapse_params = {'A_plus' : 1., 'A_minus' : 1., 'Wmin' : 0., 'Wmax' : 3000., 'tau_c' : 1000., 'tau_n' : 200.}
#connection parameters
exc_syn_params = {"model": "stdp_dopamine_synapse",
              "alpha": {"distribution": "uniform", "low": 0., "high": 100.}, 
              "weight": {"distribution": "uniform", "low": 200., "high": 201.},
              "delay" : 1.0}

additive_stdp_syn_params = {"model": "stdp_synapse",
              "alpha": {"distribution": "uniform", "low": 0., "high": 100.}, 
              "weight": {"distribution": "uniform", "low": 0., "high": 3000.},
              "delay" : 1.0}

inh_syn_params = {"model": "stdp_dopamine_synapse",
              "alpha": {"distribution": "uniform", "low": 0., "high": 100.}, 
              "weight": {"distribution": "uniform", "low": -3000., "high": 0.},
              "delay" : 1.0}


reward_factor = 0.01

#snake parameters

snake_corridor_width = 0.4
reset_distance = 0.2
reset_distance_side = 0.1
radius_max = 100.
radius_min = 2.

n_max = sim_time//neuronparams['t_ref'] - 10. #maximum spikes

rate = 20. #rospy rate 