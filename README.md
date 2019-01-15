# SnakeRobotSNNController
TUM Bachelor Thesis Comparison of Spiking Neural Network Reinforcement Learning Methods for Autonomous Locomotion of Snake-Like Robot by Dmitry Kochikiyan under the supervision of Zhenshan Bing, M.Sc.

* src/R-STDPSnake       - contains PyDev project 
* resources             - contains V-REP scenarios, OpenSCAD defintions, .obj meshes and textures
* bachelor-thesis-latex - contains thesis in latex, based on template by fwalch

# Abstract 

In the past decades there was a great advancement in the development of second generation of Artificial Neural Networks (ANN) which, coupled with ever-growing hardware performance, moved them from research phase to mainstream use. However, a major obstacle on the way of further expansion of ANN applications is their significant power consumption. This is due to high numbers of neurons, which means high amount of computation, needed for problem solving in such areas as autonomous robots, vehicles and mobile devices. And autonomous devices have a limited energy resource. 
A possible solution to the power draw could be ANNs of third generation called Spiking Neural Networks. They much more closely imitate biological neurons, but therefore differ significantly from conventional ANNs. Instead of processing information continuously they do so in discrete spikes imitating biological synaptic connections between neurons, which enables incorporation of spatial-temporal information. One one hand it makes them more efficient, but on the other hand it makes it difficult to apply learning algorithms developed for 2nd generation ANNs. This is the problem which current ongoing research is trying to solve. 

# Getting Started

Prerequisites:

* Latest Archlinux (on 15.01.2019) or Ubuntu 18.04 LTS
* Python 3
* NEST 2.16
* ROS Melodic Morenia
* V-REP 3.5.0

# Training

1) Start V-REP and load snakeTraining.ttt scenario
2) Start simulation
3) Start training.py

The trained weights will be written to data/rstdp_testing_data.h5, the training performance data will be written to data/rstdp_training_data.hg

# Testing

1) Start V-REP and load snakeTest.ttt scenario
2) Start simulation
3) Start controller.py

The controller reads weights from data/rstdp_testing_data.h5 and stores performance data to data/rstdp_performance_data.h5

# Using different RSTDP learning rules

To use different RSTDP learning rules, change between arm.SpikingNeuralNetwork() and mrm.SpikingNeuralNetwork() in controller.py or/and training.py

# Using different reward functions

To use different reward functions, change between self.getAreaBasedReward() and self.getApproxCenterDistanceReward() on line 213 of environment.py
