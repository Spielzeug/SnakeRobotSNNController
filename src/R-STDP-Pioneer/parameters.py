#!/usr/bin/env python

import numpy as np

dvs_resolution = [128,128]
crop_top = 40
crop_bottom = 24
resolution = [8,4]

sim_time = 50.0
t_refrac = 2.
time_resolution = 0.1
iaf_params = {}
poisson_params = {}
max_poisson_freq = 300.
max_spikes = 15.
		

w_min = 0.
w_max = 3000.
w0_min = 200.
w0_max = 201.
tau_n = 200.
tau_c = 1000.
reward_factor = 0.01
A_plus = 1.
A_minus = 1.


v_max = 1.5	
v_min = 1.
turn_factor= 0.5
turn_pre = 0
v_pre = v_max
n_max = sim_time//t_refrac - 10.

reset_distance = 0.2
rate = 20.

