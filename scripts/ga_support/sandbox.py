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
import itertools

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

def create_individual(individual_size, min_size, max_size, restrictions_counts, restrictions):
    n = individual_size
    individual = list(np.zeros(n, dtype=int))
    candidates = list(range(n))
    n_attr = np.random.randint(min_size, max_size+1)
    
    count = 0
    while count < n_attr:
        position = random.choice(range(len(candidates)))
        index = candidates.pop(position)
        
        individual[index] = 1
        count += 1
        
        removed = [index]
        if restrictions_counts[index]:
            for i, value in enumerate(restrictions[index]):
                if value and i in candidates:
                    candidates.remove(i)
                    removed.append(i)
                    
        if len(candidates) + count < min_size:
            individual[index] = 0
            count -= 1
            candidates = candidates + removed
            
        if not len(candidates):
            break
        
    return individual

def count_violations(individual, restrictions_counts, restrictions):
    violations = 0
    for i,item in enumerate(individual):
        if item and restrictions_counts[i]:
            for j, forbidden in enumerate(restrictions[i]):
                if forbidden and individual[j]:
                    violations += 1
                    
    return violations

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


def generate_binary_rep(active_positions, individual_size):
    bin_rep = np.zeros(individual_size, dtype=int)
    for pos in active_positions:
        bin_rep[pos] = 1
        
    return bin_rep

def get_combinations(n_attr, min_size, max_size):
    positions = list(range(n_attr))
    combinations = []
    for r in range(min_size, max_size+1):
        combs = itertools.combinations(positions, r)
        for c in combs:
            bin_c = generate_binary_rep(c, n_attr)
            combinations.append(bin_c)
            
    return combinations

data = pd.read_json('../files/data/data_pruned_df.json')
corr_threshold = 0.75

pop_size = 100
min_size = 3
max_size = 9

corr = data.corr()
attributes = list(corr.columns)
restrictions_counts = np.zeros(len(attributes))
restrictions = np.zeros((len(attributes), len(attributes)))
for i in range(0, len(attributes)-1):
    for j in range(i+1, len(attributes)):
        if abs(corr[attributes[i]][attributes[j]]) >= corr_threshold:
            restrictions[i][j] += 1
            restrictions[j][i] += 1
            restrictions_counts[i] += 1
            restrictions_counts[j] += 1

combs = get_combinations(len(attributes), min_size, max_size)
population = []
large = []
large_size = 5
total_violations = np.sum(restrictions_counts)
for i, ind in enumerate(combs):
    print('Generating individual %d:' % (i+1), end=' ')
    #ind = create_individual(len(attributes), min_size, max_size, restrictions_counts, restrictions)
    #ind = create_chromosome(len(attributes), min_size, max_size)
    violations = count_violations(ind, restrictions_counts, restrictions)
    print(ind, '%d attributes, violations: %d of %d' % (np.sum(ind), violations, total_violations), end=' ')
    if violations:
        print('Discarded.')
    else:
        print('Accepted.')
        population.append(ind)
        if np.sum(ind) > large_size:
            large.append(ind)

print('\nTotal of %d inviduals accepted, being %d of them with more than %d attributes.' % (len(population), len(large), large_size))
