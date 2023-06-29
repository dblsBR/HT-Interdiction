# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 11:04:17 2023

@author: daniel
"""

import networkx as nx;
#import matplotlib.pyplot as plt
#import pandas as pd;
import gurobipy as gp;
from gurobipy import GRB;
import csv;
import sys;
import time;
from datetime import datetime;
import math;
#import random;
#import itertools;
import numpy as np;

from InnerProblem import *

def solver_Pessimistic (network, budget, rate, T_Limit, summaryName):
    
    start_time = time.time(); 
    networkCSV = network+'.csv';

    # Reading network file
    with open(networkCSV, newline='') as f:
        reader = csv.reader(f);
        row1 = next(reader);
        s = int(row1[0]);             # Source node
        t = int(row1[1]);             # Sink node
        calA_level = int(row1[2]);    # Level of special arcs
    
        G = nx.DiGraph();
        data = pd.read_csv(networkCSV, skiprows=1, header=None);
        n_edge = len(data.index+1);
    
        for i in range(n_edge): 
            G.add_edge(data.iat[i,0], data.iat[i,1], capacity= data.iat[i,2], 
                    cost=data.iat[i,3], special=data.iat[i,4], level=data.iat[i,5]);  
    
    
    A = 0;
    U = G.edges[t,s]['capacity'];
    for i,j in G.edges:
        if G.edges[i,j]['special'] == 1:
            A = A + 1;
    
    ### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
    
    
    ### Optimization Model ### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    M = A;
    Mo = A;
    Me = A;
    
    #instance = 'LogFile_'+network+'_b'+str(budget)+'.txt';
    
    model = gp.Model("Pessimistic_EarlyRelax");  
    
    gamma = model.addVars(G.edges, vtype=GRB.BINARY);
    chi = model.addVars(G.nodes, vtype=GRB.CONTINUOUS, lb = -GRB.INFINITY, ub = GRB.INFINITY);
    omega = model.addVars(G.edges, vtype=GRB.CONTINUOUS, lb = 0, ub = GRB.INFINITY);
    phi = model.addVars(G.edges, vtype=GRB.CONTINUOUS, lb = -GRB.INFINITY, ub = 0);
    eta = model.addVar(vtype=GRB.CONTINUOUS, lb = -GRB.INFINITY, ub = 0);
    kappa = model.addVars(G.edges, vtype=GRB.CONTINUOUS, lb = 0, ub = GRB.INFINITY);
    delta = model.addVars(G.edges, vtype=GRB.CONTINUOUS, lb = -GRB.INFINITY, ub = 0);
    epsilon = model.addVars(G.nodes, vtype=GRB.CONTINUOUS, lb = 0, ub = GRB.INFINITY);
    pi = model.addVar(vtype=GRB.CONTINUOUS, lb = -GRB.INFINITY, ub = 0);
    nu = model.addVars(G.edges, vtype=GRB.CONTINUOUS, lb = 0, ub = GRB.INFINITY);
    psi = model.addVars(G.edges, vtype=GRB.CONTINUOUS, lb = 0, ub = GRB.INFINITY);
    xi = model.addVars(G.edges, vtype=GRB.CONTINUOUS, lb = -GRB.INFINITY, ub = 0);
    
    val = model.addVar(vtype=GRB.CONTINUOUS, lb = 0, ub = GRB.INFINITY);
    x = model.addVars(G.edges, vtype=GRB.CONTINUOUS, lb = 0, ub = GRB.INFINITY);
    z = model.addVars(G.edges, vtype=GRB.CONTINUOUS, lb = 0, ub = 1);
    
    
    ### Constraints ### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    model.addConstr(val >= gp.quicksum(psi[i,j]*G.edges[i,j]['capacity'] for i,j in G.edges) +
                    pi + gp.quicksum(epsilon[i] for i in G.nodes) + gp.quicksum(nu[i,j] for i,j in G.edges) + 
                    gp.quicksum(kappa[i,j]*G.edges[i,j]['special'] for i,j in G.edges));
    
    model.addConstr(gp.quicksum(gamma[i,j]*G.edges[i,j]['cost'] for i,j in G.edges) <= budget);
            
    model.addConstr(chi[t] - chi[s] + omega[t,s] + eta >= 0);
    
    for i,j in G.edges:
        if (G.edges[i,j]['special'] == 1):
            model.addConstr(chi[i] - chi[j] + omega[i,j] + phi[i,j] >= 0);
        elif (i != t and j!= s):
            model.addConstr(chi[i] - chi[j] + omega[i,j] >= 0);
            
    for i,j in G.edges:
        if (G.edges[i,j]['special'] == 1):
            model.addConstr(kappa[i,j] - (1/M)*phi[i,j] >= 1);
            
    model.addConstr(gp.quicksum(delta[t,j] for j in G.successors(t))-
                    gp.quicksum(delta[j,t] for j in G.predecessors(t)) + epsilon[t] + pi >= 0);
            
    model.addConstr(gp.quicksum(delta[j,s] for j in G.predecessors(s))-
                    gp.quicksum(delta[s,j] for j in G.successors(s)) + epsilon[s] - pi >= 0);
    
    for i in G.nodes:
        if i != s and i != t:
            model.addConstr(gp.quicksum(delta[i,j] for j in G.successors(i))-
                            gp.quicksum(delta[j,i] for j in G.predecessors(i)) + epsilon[i] >= 0);
                    
    for i,j in G.edges:
        model.addConstr(delta[i,j] - G.edges[i,j]['capacity']*xi[i,j] + nu[i,j] >= 0);
        model.addConstr(psi[i,j] <= omega[i,j]);
        model.addConstr(psi[i,j] <= (1-gamma[i,j])*Mo);
        model.addConstr(psi[i,j] >= omega[i,j] - Mo*gamma[i,j]);
        model.addConstr(xi[i,j] >= eta);
        model.addConstr(xi[i,j] >= -(1-gamma[i,j])*Me);
        model.addConstr(xi[i,j] <= eta + gamma[i,j]*Me);
        
    model.setObjective(val, GRB.MINIMIZE); 
    model.setParam("IntegralityFocus",1);
    model.setParam("MIPFocus", 3);
    #model.setParam('NodefileStart', 0.5)    # Memore Issues
    #model.setParam("NumericFocus",2);
    model.setParam('TimeLimit', T_Limit); 
    model.update();
    
    #model.setParam("LogToConsole", 0);
    model.setParam("OutputFlag", 0);
    #model.setParam("LogFile", instance);
    model.optimize();
    
    status = model.status;
    
    ### Solving auxiliary (inner) problem ###
    
    x, z = InnerProblem (gamma, G, s, t, M);
    
    ##########################################
    
    end_time = time.time();
    run_time = round(end_time - start_time, 2);
    
    now = datetime.now();
    
    obj = model.objVal;
    LB = model.objBound;
    sol = A - obj;
    OptGap = round(model.MIPGap, 2);
    
    ### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ####
    
    ### Print to the screen and to result file #######################
    
    file = open('Solver_EarlyRelax_'+network+'_b'+str(budget)+'_r'+str(rate)+'.txt', "w");
    file.write('Instance: %s, budget %g, rate %g \n' %(network, budget, rate));
    file.write('Instance executed at: %s \n\n' %now.strftime("%c"));
    
    file.write('Number of Nodes: %g \n' % (t+1));
    file.write('Number of Arcs: %g \n' % G.number_of_edges());
    file.write('Level of special set: %g \n' % calA_level);
    file.write('Budget: %g' % budget +'\n\n');
    
    
    print('\n');
    print('Instance: %s, budget %g, rate %g \n' %(network, budget, rate));
    if status == 2:
        print('Status: Optimal');
        print('Number of special arcs without flow: %g' % sol);
        print('Number of special arcs with flow: %g' % obj);
        
        file.write('Status: Optimal\n');
        file.write('Number of special arcs without flow: %g \n' % sol);
        file.write('Number of special arcs with flow: %g \n' % obj);
        
    elif status == 9:
        print('Status: Time Limit');
        print('Number of special arcs without flow: %g' % sol);
        print('Number of special arcs with flow: %g' % obj);     
        print('Optimality Gap: %g' % OptGap);
        
        file.write('Status: Time Limit \n');
        file.write('Number of special arcs without flow: %g \n' % sol);
        file.write('Number of special arcs with flow: %g \n' % obj);     
        file.write('Optimality Gap: %g \n' % OptGap);
              
    else:
        print('Status: %g', status);
        file.write('Status: %g \n', status);
    
    print('\nMax-Flow: %g' %x[t,s]);
    file.write('Max-Flow: %g \n' %x[t,s]);
    
    print('run time: %g sec \n' %run_time);
    file.write('run time: %g sec \n' %run_time);
    
    file.write('Level 0 Capacities: %g \n\n ' %G.edges[s,1]['capacity']);
    
    print('Intediction:');
    for i,j in G.edges:
        if gamma[i,j].x > 0.000001:
            print("arc (%g,%g), gamma = %g " %(i,j, gamma[i,j].x));
    print('\n');
    
    
    lev1 = 0;
    lev2 = 0;
    lev3 = 0;
    other_level = 0;
    
    file.write('\nInterdiction plan: \n');
    
    key1 = False;
    key2 = False;
    key3 = False;
    
    for i, j in G.edges: 
        if gamma[i,j].x > 0.0000001:
            if G.edges[i,j]["level"] == 1:
                if key1 == False:
                    file.write("Level 1:" +'\n');
                    key1 = True;
                file.write('Arc (%s,%s) \n' %(i,j));
                lev1 += 1;
            elif G.edges[i,j]["level"] == 2:
                if key2 == False:
                    file.write('Level 2: \n');
                    key2 = True;
                file.write('Arc (%s,%s) \n' %(i,j));
                lev2 += 1;
            elif G.edges[i,j]["level"] == 3:
                if key3 == False:
                    file.write('Level 3: \n');
                    key3 = True;
                file.write('Arc (%s,%s) \n' %(i,j));
                lev3 += 1;
            else:
                file.write('Other Levels: \n');
                file.write('Arc (%s,%s) \n' %(i,j));
                other_level += 1;
                
    file.write('\nSpecial arcs with flow : \n');    
    for i, j in G.edges:
        if G.edges[i,j]['special'] == 1:
            if x[i,j] > 0.0000001:
                file.write('Arc (%s,%s), Flow: %f \n' %(i,j, x[i,j]));
    
    
    
    file.write('\n');
    file.close();
    
    rowFields = [network, budget, calA_level, (t+1), G.number_of_edges(), OptGap, obj, x[t,s], lev1, lev2, lev3,
                 other_level, run_time];
    
    with open(summaryName, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile);
        csvwriter.writerow(rowFields);
        csvfile.close();
