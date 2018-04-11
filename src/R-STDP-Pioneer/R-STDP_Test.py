#!/usr/bin/env python
from __future__ import print_function

import nest
import numpy as np
import pylab

class SpikingNeuralNetwork():
	def __init__(self):
		self.n_poisson = 100
		self.f_poisson_max = 50
		self.f_poisson_min = 0
		self.f_target_max = 100
		self.f_target_min = 20
		self.n_neuron = 100
		self.time_resolution = 1.0
		self.sim_resolution = 0.1
		self.pre_time = 3000
		self.post_time = 30000
		self.tau_f = 2000.
		self.r_factor = 0.05

		nest.set_verbosity('M_WARNING')
		nest.ResetKernel()
		nest.SetKernelStatus({"resolution" : self.sim_resolution})
		
		self.poisson_params = []
		for i in range(self.n_poisson):
			rate = float(np.random.randint(self.f_poisson_min,self.f_poisson_max))
			self.poisson_params.append({"rate": rate})
		self.spike_generators = nest.Create("poisson_generator", self.n_poisson, params=self.poisson_params)

		self.neuron_pre = nest.Create("parrot_neuron", self.n_poisson)

		self.iaf_params = {}
		self.neuron_post = nest.Create("iaf_neuron", self.n_neuron, params=self.iaf_params)
		
		self.syn_dict = {"model": "stdp_dopamine_synapse",
						"weight": {"distribution": "uniform", "low": self.w_min, "high": self.w_max}}
		self.vt = nest.Create("volume_transmitter")
		nest.SetDefaults("stdp_dopamine_synapse", {"vt": self.vt[0], "tau_n": self.tau_n, "Wmin": self.w_min, "Wmax": self.w_max, "A_plus": p.A_plus, "A_minus": p.A_minus})

		self.spike_detector = nest.Create("spike_detector", self.n_neuron, params={"withtime": True})

		self.f_target = []
		for i in range(self.n_neuron):
			rate = float(np.random.randint(self.f_target_min,self.f_target_max))
			self.f_target.append(rate)
		
		nest.Connect(self.spike_generators, self.neuron_pre, "one_to_one")
		nest.Connect(self.neuron_pre, self.neuron_post, "all_to_all", syn_spec=self.syn_dict)
		nest.Connect(self.neuron_post, self.spike_detector, "one_to_one")

		#self.multimeter = nest.Create("multimeter")
		#nest.SetStatus(self.multimeter, {"withtime":True, "record_from":["V_m"]})
		#nest.Connect(self.multimeter, [self.neuron_post[0]])

		self.detector = nest.Create("spike_detector", params={"withtime": True})
		nest.Connect([self.neuron_post[0]], self.detector)
		
		self.f_output = np.zeros(self.n_neuron)
		self.distance = 0

		for i in range(self.pre_time):
			print("Pre-Simulation step: ", str(i), end='\r')
			output_spikes = self.simulate()
			self.update_leaky_integrator(output_spikes)

		for i in range(self.post_time):
			print("Post-Simulation step: ", str(i), "Distance:",  str(self.distance), end='\r')
			output_spikes = self.simulate()
			self.update_leaky_integrator(output_spikes)
			r = self.update_distance()
			self.set_reward(r*self.r_factor)

	def simulate(self):
		nest.SetStatus(self.spike_detector, {"n_events": 0})
		nest.Simulate(self.time_resolution)
		data = np.array(nest.GetStatus(self.spike_detector,keys="events"))
		output_spikes = []
		for neuron in data:
			output_spikes.append(len(neuron["times"]))
		return output_spikes

	def update_leaky_integrator(self, output_spikes):
		for i in range(len(output_spikes)):
			self.f_output[i] = self.f_output[i]*np.exp(-self.time_resolution/self.tau_f)
			if output_spikes[i]>0:
				 self.f_output[i] += (float(output_spikes[i])/self.tau_f)

	def get_distance(self):
		d = 0
		for i in range(self.f_output.shape[0]):
			d += ((self.f_output[i]*1e3) - self.f_target[i])**2
		return np.sqrt(d)

	def update_distance(self):
		new_distance = self.get_distance()
		r = np.sign(self.distance - new_distance)
		self.distance = new_distance
		return r

	def set_reward(self, r):
		conn = nest.GetConnections(target=self.neuron_post)
		nest.SetStatus(conn, {"n": r})
		





snn = SpikingNeuralNetwork()
#dmm = nest.GetStatus(snn.multimeter)[0]
#Vms = dmm["events"]["V_m"]
#ts = dmm["events"]["times"]
#pylab.figure(1)
#pylab.plot(ts, Vms)
#pylab.show()

print(nest.GetStatus(snn.detector,keys="n_events")[0])

print(snn.f_output)