#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 15:17:20 2018

@author: marcos
"""

import pandas as pd
import numpy as np
import random as rnd

def create_restrictions(json_file):
    df = pd.read_json(json_file)
    corr = df.corr()
    
    attributes = list(df.columns)
    restrictions = []
    
    for i in range(0, len(attributes)-1):
        for j in range(i+1, len(attributes)):
            if abs(corr[attributes[i]][attributes[j]]) >= corr_threshold:
                restriction = np.zeros(len(attributes), dtype=int)
                restriction[i] = 1
                restriction[j] = 1
                restrictions.append(restriction)
    restrictions = np.array(restrictions)
    
    return attributes, restrictions


def create_individual(ind_size=9, min_size=3, max_size=6):
    individual = np.zeros(ind_size, dtype=int)
    n_activated = rnd.randint(min_size, max_size)
    indexes = rnd.sample(range(ind_size), n_activated)
    for i in indexes:
        individual[i] = 1
        
    return individual

corr_threshold = 0.75
json_file = 'files/data/data_pruned_df.json'
n_tests = 10

attributes, restrictions = create_restrictions(json_file)
for n in range(n_tests):
    print('Test #%d' % (n+1))
    individual = create_individual(len(attributes))
    print('\tIndividual:', individual)
    
    violations = 0
    for i in range(len(restrictions)):
        violated = np.sum(np.bitwise_and(individual, restrictions[i])) >= 2
        if violated:
            print('\t           ', restrictions[i])
            violations += 1
            
    print('\n\t%d of %d restrictions violated.' % (violations, len(restrictions)))
