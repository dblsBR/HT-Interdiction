# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 11:05:25 2023

@author: daniel
"""

import networkx as nx;
#import matplotlib.pyplot as plt
import pandas as pd;
import gurobipy as gp;
from gurobipy import GRB;
import csv;
import sys;
#import time;
#from datetime import datetime;
import math;
#import random;
#import itertools;
import numpy as np;



# Max Problem (to obtain the values of x and z given an interdiction)

def InnerProblem (gamma, G, s, t, M):
    
    max_model = gp.Model("Max_z");
    
    x = max_model.addVars(G.edges, vtype=GRB.CONTINUOUS, lb = 0, ub = GRB.INFINITY);
    z = max_model.addVars(G.edges, vtype=GRB.CONTINUOUS, lb = 0, ub = 1);
    alpha = max_model.addVars(G.nodes, vtype=GRB.CONTINUOUS, lb = 0, ub = 1);
    theta = max_model.addVars(G.edges, vtype=GRB.CONTINUOUS, lb = 0, ub = 1);
    
    sum_z = max_model.addVar(vtype=GRB.CONTINUOUS, lb = 0, ub = GRB.INFINITY);
            
    max_model.addConstrs(gp.quicksum(x[j,i] for i in G.successors(j))
                         - gp.quicksum(x[i,j] for i in G.predecessors(j)) == 0 for j in G.nodes);
            
    for i,j in G.edges:
        max_model.addConstr(x[i,j] - (1-gamma[i,j].x)*G.edges[i,j]['capacity'] <= 0);
            
    for i,j in G.edges:
        max_model.addConstr(alpha[i] - alpha[j] + theta[i,j] >= 0);
            
    max_model.addConstr(alpha[t] - alpha[s] >= 1);
            
    max_model.addConstr(x[t,s] - gp.quicksum((1-gamma[i,j].x)*G.edges[i,j]['capacity']*theta[i,j]
                                                     for i,j in G.edges) >= 0);
            
    for i,j in G.edges:
        if (G.edges[i,j]['special'] == 1):
            max_model.addConstr(z[i,j] == 0);
            max_model.addConstr(x[i,j] - (1/M)*z[i,j] >= 0);
            
    max_model.addConstr(sum_z <= gp.quicksum(z[i,j]*G.edges[i,j]['special'] for i,j in G.edges));
            
    max_model.setObjective(sum_z, GRB.MAXIMIZE); 
            
    max_model.setParam("IntegralityFocus",1);
    #max_model.setParam("NumericFocus",2);       
    #max_model.setParam('TimeLimit', T_Lim);
            
    max_model.update();
    max_model.setParam("OutputFlag", 0);
    max_model.optimize();
    
    X = {};
    Z = {};
    
    for i,j in G.edges:
        X[i,j] = x[i,j].x;
        Z[i,j] = z[i,j].x;
      
    return X, Z;