# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 11:02:27 2023

@author: daniel
"""

import networkx as nx;
#import matplotlib.pyplot as plt
#import pandas as pd;
#import gurobipy as gp;
#from gurobipy import GRB;
import csv;
#import sys;
#import time;
#from datetime import datetime;
#import math;
#import random;
#import itertools;
#import numpy as np;


from pessimistic_EarlyRelax import *
#from InnerProblem import *


n_Networks = 1;
Budget = [5];
Rate = [1];

T_Limit = 1800;

summaryName = "Solver_EarlyRelax_Summary.csv"
file_summary = open(summaryName, "w");
file_summary.write('Instance\t, Budget\t, Cal_A\t, Nodes\t, Arcs\t, OptGap\t,');
file_summary.write('Obj_val\t, Flow\t, Level_1\t, Level_2\t, Level_3\t, Other_Lev\t, Run_Time\n');
file_summary.close();

for n in range(1, n_Networks+1):
    network = 'Net'+str(n);
    
    for budget in Budget:
        
        for rate in Rate:
            pessimistic_EarlyRelax(network, budget, rate, T_Limit, summaryName);