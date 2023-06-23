# GIPsimulator
This repository contains code for simulating group identification problems. In the file GIP.py you will find several functions useful for Group Identification Problems, such as functions for simulating all possible profiles or all possible opinions. In addition, you can find sever Aggregation Rules in this file, which take as an input a profile of agents and produce a vector of selected agents as output.

The file jpetpref.py contains code for running a simulation that uniformly generates random profiles and calculates the frequency of strategic manipulation.

The file GIP.py contains all functions needed to construct and simulate Group Identification Problems. In this file there are functions that calculate the outcome of multiple voting rules given a profile. This file also contains multiple functions for determining whether one outcome is preferred to another one based on a preference relation. In addition, it contains multiple "manipulable" functions, which computes whether a profile is susceptible to manipulation given a certain preference. 
