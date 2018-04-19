#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 14:48:31 2018

@author: marcos
"""
import random
import numpy as np
import copy
from operator import attrgetter
import pandas as pd

class Chromosome(object):
    """ Chromosome class that encapsulates an individual's fitness and solution
    representation.
    """
    def __init__(self, genes):
        """Initialise the Chromosome."""
        self.genes = genes
        self.fitness = 0
        self.hash = ''.join([str(gene) for gene in self.genes])

    def __repr__(self):
        """Return initialised Chromosome representation in human readable form.
        """
        return repr(self.genes) + ': ' + str(self.fitness)
    
    def evaluate(self, weights):
        self.fitness = np.sum(np.array(weights) * self.genes)

def create_chromosome(individual_size, min_size, max_size):
    individual = list(np.zeros(individual_size, dtype=int))
    indexes = list(range(individual_size))
    n_attr = np.random.randint(min_size, max_size+1)
    
    activated = random.sample(indexes, n_attr)
    
    for i in activated:
        individual[i] = 1
        
    return individual

def simulate_elite():
    pop_size = 100
    min_size = 3
    max_size = 9
    individual_size = 9
    weights = [12, 11, 8, 7, 21, 19, 3, 8, 4]
    elite_size = 6
    
    elite = []
    
    population = []
    for _ in range(pop_size):
        chromosome = Chromosome(create_chromosome(individual_size, min_size, max_size))
        chromosome.evaluate(weights)
        population.append(chromosome)
        
        if chromosome.hash not in [obj.hash for obj in elite]:
            if len(elite) < elite_size:
                elite.append(copy.deepcopy(chromosome))
                elite.sort(key=attrgetter('fitness'), reverse=True)
                print(elite)
                print(len(elite))
                print()
            else:
                lower_bound = min(elite, key=attrgetter('fitness')).fitness
                if chromosome.fitness > lower_bound:
                    elite.pop(len(elite)-1)
                    elite.append(copy.deepcopy(chromosome))
                    elite.sort(key=attrgetter('fitness'), reverse=True)
                    print(elite)
                    print(len(elite))
                    print()
                
    
    """for individual in population:
        print(individual)
    print('==========ELITE========')
    for individual in elite:
        print(individual)"""


data = pd.read_json('../files/data/data_pruned_df.json')
corr_threshold = 0.75

corr = data.corr()
attributes = list(corr.columns)
counts = np.zeros(len(attributes))
restrictions = np.zeros((len(attributes), len(attributes)))
for i in range(0, len(attributes)-1):
    for j in range(i+1, len(attributes)):
        if abs(corr[attributes[i]][attributes[j]]) >= corr_threshold:
            restrictions[i][j] += 1
            restrictions[j][i] += 1
            counts[i] += 1
            counts[j] += 1
            
print(restrictions)
print(counts)

