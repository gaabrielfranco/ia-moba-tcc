#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 21:06:32 2019

@author: dpi
"""

import numpy as np
import random

class Test(object):
    def __init__(self, min_size, max_size, max_possible, mutation_percentage):
        self.min_size = min_size
        self.max_size = max_size
        self.max_possible = max_possible
        self.mutation_percentage = mutation_percentage
        
    def analyse_chromossome(self, individual):
        item_count = 0
        zeros = []
        ones = []
        for i,item in enumerate(individual):
            item_count += item
            if item:
                ones.append(i)
            else:
                zeros.append(i)
                
        return item_count, ones, zeros
    
    def mutate_perc(self, individual):
        item_count, ones, zeros = self.analyse_chromossome(individual)
        n_affected_attr = int(np.round(self.mutation_percentage * self.max_possible))
        
        n_add = random.randint(0, n_affected_attr)
        n_rem = n_affected_attr - n_add
        new_count = item_count + n_add - n_rem
        
        print('initial: add %d, remove %d' % (n_add, n_rem), end=' ')
        
        # Individual would have less attributes than the mimimum allowed
        if new_count < self.min_size:
            exceeded = self.min_size - new_count
            n_rem -= exceeded
            n_add += exceeded
            print('bellow limits')
        # Individual will have more attributes than the maximum allowed
        elif new_count > self.max_size:
            exceeded = new_count - self.max_size
            n_rem += exceeded
            n_add -= exceeded
            print('over limits')
        # Otherwise, the size of new solution is inside bounds: not to do
        else:
            print('inside bounds')
        
        print('adjust:  add %d, remove %d' % (n_add, n_rem))
            
        # Applying mutation
        indexes = random.sample(zeros, n_add)
        for index in indexes:
            individual[index] = 1
        
        indexes = random.sample(ones, n_rem)
        for index in indexes:
            individual[index] = 0
            
    def create_individual(self):
        n = self.max_possible
        individual = list(np.zeros(n, dtype=int))
        candidates = list(range(n))
        n_attr = np.random.randint(self.min_size, self.max_size+1)
        
        count = 0
        while count < n_attr:
            position = random.choice(range(len(candidates)))
            index = candidates.pop(position)
            
            individual[index] = 1
            count += 1
            
        return individual

n_individuals = 20
    
test = Test(3, 6, 36, 0.1)
population = []
for i in range(n_individuals):
    population.append(test.create_individual())
    print('Individual:')
    print(population[i])
    print('size: %d' % np.sum(population[i]))
    test.mutate_perc(population[i])
    print('Becomes:')
    print(population[i])
    print('size: %d' % np.sum(population[i]))
    print()
    
