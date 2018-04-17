# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 19:28:10 2018

@author: marcos
"""

import numpy as np

def euc_2d(c1, c2):
    return np.round(np.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2))

def cost(perm, cities):
    distance = 0
    for i, c1 in enumerate(perm):
        if i == len(perm)-1:
            c2 = perm[0]
        else:
            c2 = perm[i+1]
        distance += euc_2d(cities[c1], cities[c2])
    
    return distance
    
def stochastic_two_opt(permutation):
    perm = np.array(permutation)
    c1 = np.random.randint(0, len(perm))
    exclude = [c1]
    if c1 == 0:
        exclude.append(len(perm)-1)
    else:
        exclude.append(c1-1)
    if c1 == len(perm)-1:
        exclude.append(0)
    else:
        exclude.append(c1+1)
    
    c2 = np.random.randint(0, len(perm))
    while c2 in exclude:
        c2 = np.random.randint(0, len(perm))
        
    if c2 < c1:
        c1, c2 = c2, c1
        
    perm[c1:c2+1] = np.flip(perm[c1:c2+1], axis=0)
    
    return list(perm)

def local_search(best, cities, max_no_improv):
    count = 0
    while count < max_no_improv:
        candidate = {'vector': stochastic_two_opt(best['vector'])}
        candidate['cost'] = cost(candidate['vector'], cities)
        if candidate['cost'] < best['cost']:
            count = 0
        else:
            count += 1
        if candidate['cost'] < best['cost']:
            best = candidate
    return best
    
def construct_randomized_greedy_solution(cities, alpha):
    candidate = {}
    candidate['vector'] = [np.random.randint(0, len(cities))]
    allCities = np.array(range(0, len(cities)))
    while len(candidate['vector']) < len(cities):
        candidates = [c for c in allCities if c not in candidate['vector']]
        costs = []
        for i in range(0, len(candidates)):
            costs.append(euc_2d(cities[candidate['vector'][len(candidate['vector'])-1]], cities[i]))
        rcl = []
        maximum = np.max(costs)
        minimum = np.min(costs)
        for i,c in enumerate(costs):
            if c <= minimum + alpha*(maximum - minimum):
                rcl.append(candidates[i])
        candidate['vector'].append(rcl[np.random.randint(0, len(rcl))])
    candidate['cost'] = cost(candidate['vector'], cities)
    return candidate

def grasp(cities, max_iter, max_no_improv, alpha):
    best = {'vector': [], 'cost': float('inf')}
    iteration = 0
    while iteration < max_iter:
        candidate = construct_randomized_greedy_solution(cities, alpha)
        candidate = local_search(candidate, cities, max_no_improv)
        if candidate['cost'] < best['cost']:
            best = candidate
        print('\tIteration: %d, best=%.4f' % (iteration, best['cost']))
        iteration += 1
    return best

def strRep(vector):
    newVector = []
    for v in vector:
        newVector.append(str(v))
    s = '[' + ', '.join(newVector) + ']'
    
    return s

def main():
    problemName = 'berlin52'
    problem = [[565,575],[25,185],[345,750],[945,685],[845,655],
       [880,660],[25,230],[525,1000],[580,1175],[650,1130],[1605,620],
       [1220,580],[1465,200],[1530,5],[845,680],[725,370],[145,665],
       [415,635],[510,875],[560,365],[300,465],[520,585],[480,415],
       [835,625],[975,580],[1215,245],[1320,315],[1250,400],[660,180],
       [410,250],[420,555],[575,665],[1150,1160],[700,580],[685,595],
       [685,610],[770,610],[795,645],[720,635],[760,650],[475,960],
       [95,260],[875,920],[700,500],[555,815],[830,485],[1170,65],
       [830,610],[605,625],[595,360],[1340,725],[1740,245]]    
    
    max_iter = 50
    max_no_improv = 50
    greediness_factor = 0.3
    
    print('Running GRASP for %s (%d cities) max_iter=%d, max_no_improv=%d, and greediness_factor=%.2f' % (problemName, len(problem), max_iter, max_no_improv, greediness_factor))
    best = grasp(problem, max_iter, max_no_improv, greediness_factor)
    print('\nDone. Best solution: c=%.4f, v=%s' % (best['cost'], strRep(best['vector'])))
    
if __name__ == '__main__':
    main()
