#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 23:36:28 2018

@author: marcos
"""

from pyeasyga import pyeasyga as ga
import argparse

def fitness(individual, data):
    values, weights = 0, 0
    for selected, box in zip(individual, data):
        if selected:
            values += box.get('value')
            weights += box.get('weight')
    if weights > 15:
        values = 0
    
    return values
    
def print_solution(individual, data):
    values = individual[0]
    solution = individual[1]
    s = 'solution: ['
    weights = 0
    boxes = []
    for selected, box in zip(solution, data):
        if selected:
            boxes.append(box.get('name'))
            weights += box.get('weight')
    
    s += ', '.join(boxes) + '], profit: %d, total weight: %d' % (values, weights)
    
    print(s)

def main():
    parser = argparse.ArgumentParser(prog='ag.py', description='AG for feature selection')
    parser.add_argument('--ngen', type=int, default=100, help='Number of generations (default=100)')
    parser.add_argument('--mu', type=int, default=50, help='Population size (default=50)')
    parser.add_argument('--cxpb', type=float, default=0.8, help='Probability of crossing over (default=0.8)')
    parser.add_argument('--mutpb', type=float, default=0.2, help='Probability of mutating (default=0.2)')
    parser.add_argument('--no_elite', '-noel', action='store_false', help='No elistism (default=False)')
    parser.add_argument('--minimise', '-min', action='store_true', help='Minimise fitness (default=False)')
    args = parser.parse_args()
    maximise = not args.minimise
    elitism = not args.no_elite
    
    data = [{'name': 'box1', 'value': 4, 'weight': 12},
        {'name': 'box2', 'value': 2, 'weight': 1},
        {'name': 'box3', 'value': 10, 'weight': 4},
        {'name': 'box4', 'value': 1, 'weight': 1},
        {'name': 'box5', 'value': 2, 'weight': 2}]
    
    ag = ga.GeneticAlgorithm(data, population_size=args.mu, generations=args.ngen, crossover_probability=args.cxpb, mutation_probability=args.mutpb, elitism=elitism, maximise_fitness=maximise)
    ag.fitness_function = fitness
    ag.run()
    
    print('Best:', end=' ')
    print_solution(ag.best_individual(), data)
    
    print('\nLast generation:')
    for i,ind in enumerate(ag.last_generation()):
        print('%d -> ' % i, end='')
        print_solution(ind, data)
    
if __name__ == '__main__':
    main()
