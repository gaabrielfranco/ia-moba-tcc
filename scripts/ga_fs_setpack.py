#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### Own implementation of GA, adapted from pyeasyga
from modules.ga import GeneticAlgorithm
import argparse
from modules.data import read_data
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import sklearn.feature_selection as fs
import numpy as np
import time
import random
from operator import attrgetter

### Function for formatting time in human readable format
def get_formatted_time(s):
    decimal_part = s - int(s)
    
    s = int(s)
    
    seconds = s % 60

    s = s // 60
    minutes = s % 60

    s = s // 60
    hours = s % 24

    days = s // 24

    if days:
        d = '%dd ' % days
    else:
        d = ''

    return '%s%02dh%02dm%02d.%ds' % (d, hours, minutes, seconds, decimal_part)

### Classes for modelling the problem
class BaseProblem(object):
    def __init__(self, data, min_size, max_size, corr_threshold, maximise=True):
        self.data = data
        self.min_size = min_size
        self.max_size = max_size
        self.maximise = maximise
        self.hash = {}
        self.init_pop_hash = {}
        ### Restrictions creation
        self.attributes = list(self.data.columns)
        self.restrictions = np.zeros((len(self.attributes), len(self.attributes)))
        self.restrictions_counts = np.zeros(len(self.attributes))
        self.corr_threshold = corr_threshold
        self.create_restrictions()
        
    def create_restrictions(self):
        corr = self.data.corr()
        for i in range(0, len(self.attributes)-1):
            for j in range(i+1, len(self.attributes)):
                if abs(corr[self.attributes[i]][self.attributes[j]]) >= self.corr_threshold:
                    self.restrictions[i][j] += 1
                    self.restrictions[j][i] += 1
                    self.restrictions_counts[i] += 1
                    self.restrictions_counts[j] += 1
        
    def create_individual(self, _):
        n = len(self.attributes)
        individual = list(np.zeros(n, dtype=int))
        candidates = list(range(n))
        n_attr = np.random.randint(self.min_size, self.max_size+1)
        
        count = 0
        while count < n_attr:
            position = random.choice(range(len(candidates)))
            index = candidates.pop(position)
            
            individual[index] = 1
            count += 1
            
            if self.restrictions_counts[index]:
                for i in self.restrictions[index]:
                    if self.restrictions[index][i]:
                        candidates.remove(i)
                        
            if len(candidates) - count < self.min_size:
                ### CHECK WHETHER IS POSSIBLE TO CREATE A FEASIBLE SOLUTION WHITHOUT VIOLATING
                ### SIZE LIMITS CONSIDERING THE CURRENT PARTIAL SOLUTION
                print('Opa')
            
        return individual
        
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
        
    def mutate(self, individual):
        item_count, ones, zeros = self.analyse_chromossome(individual)
        
        if item_count == self.min_size:
            ### If minimum size, necessarily include one item to the solution
            mutate_index = random.choice(zeros)
            individual[mutate_index] = 1
        elif item_count == self.max_size:
            ### If maximum size, necessarily remove one item from the solution
            mutate_index = random.choice(ones)
            individual[mutate_index] = 0
        else:
            ### Otherwise, flip one item at random
            mutate_index = random.randrange(len(individual))
            individual[mutate_index] = (0, 1)[individual[mutate_index] == 0]
            
    def crossover(self, parent_1, parent_2):
        
        allowed_positions = []
        for i in range(len(parent_1)):
            count_1 = np.sum(parent_1[:i+1] + parent_2[i+1:])
            count_2 = np.sum(parent_2[:i+1] + parent_1[i+1:])
            
            limits_1 = count_1 >= self.min_size and count_1 <= self.max_size
            limits_2 = count_2 >= self.min_size and count_2 <= self.max_size
            
            if limits_1 and limits_2:
                allowed_positions.append(i)
                
        if len(allowed_positions):
            index = random.choice(allowed_positions)
            child_1 = parent_1[:index+1] + parent_2[index+1:]
            child_2 = parent_2[:index+1] + parent_1[index+1:]
            return child_1, child_2
        else:
            self.mutate(parent_1)
            self.mutate(parent_2)
            return self.crossover(parent_1, parent_2)
        
    def binary_selection(self, population):
        members = random.sample(population, 2)
        members.sort(key=attrgetter('fitness'), reverse=self.maximise)
        return members[0]
    
    def roulette_selection(self, population):
        maximum = sum(individual.fitness for individual in population)
        pick = random.uniform(0, maximum)
        current = 0
        for individual in population:
            current += individual.fitness
            if current > pick:
                return individual
        
    def get_individual_str(self, individual):
        return ''.join([str(i) for i in individual])
        
    def check_hash(self, individual):
        individual_str = self.get_individual_str(individual)
        
        if individual_str in self.hash:
            return self.hash[individual_str]
            
        return None
        
    def add_to_hash(self, individual, evaluation):
        individual_str = self.get_individual_str(individual)
        
        self.hash[individual_str] = evaluation

class VarianceProblem(BaseProblem):
    def __init__(self, data, min_size, max_size, corr_threshold, maximise=True):
        ### Run superclass constructor
        super(VarianceProblem, self).__init__(data, min_size, max_size, corr_threshold, maximise=maximise)
        print('\nRunning variance problem...\n')

    ### Get variances for attributes
    def get_variances(self, data):
        sel = fs.VarianceThreshold()
        sel.fit(data)
        return np.array(sel.variances_)
        
    ### Plot variances
    def plot_variances(self, show=False, save_file=None):
        variances = self.get_variances(self.data)
        
        ### Sorting data by their variance
        values = []
        names = []
        for i, c in enumerate(self.data.columns):
            pos = 0
            while pos < len(values) and values[pos] >= variances[i]:
                pos += 1
            values.insert(pos, variances[i])
            names.insert(pos, c)
            
        with plt.style.context('seaborn-whitegrid'):
            plt.bar(names, values)
            plt.title('Variance for Each Normalized Feature')
            plt.legend()
            plt.ylabel('Variance')
            plt.xlabel('Attributes')
            if save_file is not None:
                plt.savefig(save_file)
            if show:
                plt.show()
        
    ### Fitness function
    def fitness(self, individual, data):
        evaluation = self.check_hash(individual)
        if evaluation is not None:
            return evaluation
            
        att_sel = []
        n_selected = 0
        for selected, attr in zip(individual, list(data.columns)):
            if selected:
                n_selected += 1
                att_sel.append(attr)
        if n_selected < self.min_size or n_selected > self.max_size:
            evaluation = 0.0
        else:
            evaluation = np.average(self.get_variances(data[att_sel]))
            
        self.add_to_hash(individual, evaluation)
        
        return evaluation
        
class ClusteringProblem(BaseProblem):
    def __init__(self, k, metric, seed, data, min_size, max_size, corr_threshold, maximise=True):
        ### Run superclass constructor
        super(ClusteringProblem, self).__init__(data, min_size, max_size, corr_threshold, maximise=maximise)
        self.metric = metric
        self.k = k
        self.min_size = min_size
        self.max_size = max_size
        if seed < 0:
            self.seed = None
        else:
            self.seed = seed
        self.km = KMeans(n_clusters=self.k, random_state=self.seed, n_jobs=-1)
        self.labels = None
        print('\nRunning %s problem...\n' % self.metric)
        
    ### Clustering
    def clusterization(self, data):
        labels = self.km.fit_predict(data)
        
        if self.metric == 'inertia':
            return self.km.inertia_
        elif self.metric == 'silhouette-euclidean':
            return silhouette_score(data, labels)
        else:
            return silhouette_score(data, labels, metric='cosine')
            
    ### Fitness function
    def fitness(self, individual, data):
        evaluation = self.check_hash(individual)
        if evaluation is not None:
            return evaluation
            
        att_sel = []
        n_selected = 0
        for selected, attr in zip(individual, list(data.columns)):
            if selected:
                n_selected += 1
                att_sel.append(attr)
        if n_selected < self.min_size or n_selected > self.max_size:
            if self.metric == 'inertia':
                evaluation = float('inf')
            else:
                evaluation = 0.0
        else:
            evaluation = self.clusterization(data[att_sel])
        
        self.add_to_hash(individual, evaluation)
        
        return evaluation

### Function to print and individual (solution)        
def print_solution(individual, data):
    evaluation = individual[0]
    solution = individual[1]
    s = 'solution: ['
    att_sel = []
    for selected, attr in zip(solution, list(data.columns)):
        if selected:
            att_sel.append(attr)
    
    s += ', '.join(att_sel) + '], evaluation: %f' % (evaluation)
    
    print(s)
    
### Functions to persist solution into file
def str_representation(individual):
    evaluation = individual[0]
    solution = individual[1]
    att_sel = []
    for selected in solution:
        att_sel.append('%d' % selected)
    s = '%f;' % evaluation
    s += ';'.join(att_sel) + '\n'
    
    return s
    
def save_solution(last_generation, data, time, max_no_improv, max_gen_reached, args):
    s = 'elapstime;k;seed;metric;ngen;pop;cxpb;mutpb;elite_size;min_size;max_size;outliers;max_no_improv;max_gen_reached\n'
    s += '%f;%d;%d;%s;%d;%d;%f;%f;%d;%d;%d;%d;%d;%d\n' % (time, args.k, args.seed, args.metric, args.ngen, args.pop, args.cxpb, args.mutpb, args.elsize, args.mins, args.maxs, args.wo, max_no_improv, max_gen_reached)
    
    s += 'last_generation\n'    
    
    head = ['evaluation']
    for i in range(len(data.columns)):
        head.append(data.columns[i])
    head = ';'.join(head)
    s += head + '\n'
    
    for ind in last_generation:
        s += str_representation(ind)
    
    if args.lang == 'pt':
        s.replace('.', ',')
    
    fp = open(args.csv_file, 'w')
    fp.write(s)
    fp.close()
    
        
### Main function
def main():
    ### Parsing command line arguments
    parser = argparse.ArgumentParser(description='Feature selection tool, using Genetic Algorithm (Problem Modeled as Set Packing)')
    parser.add_argument('csv_file', help='csv file to save output data')
    parser.add_argument('--lang', default='en', help='Whether use . or , as floating point number decimal separator in output. If lang=en, uses dot if lang=pt, uses comma (default=en)')
    parser.add_argument('--k', type=int, default=10, help='Number of clusters (default=10)')
    parser.add_argument('--seed', type=int, default=-1, help='Random seed (default=-1). Use -1 for totally uncontrolled randomness')
    parser.add_argument('--metric', default='se', choices=['se', 'sc', 'i', 'v'], help='Metric to optimize: se | sc | i | v (silhouette with euclidean distance, silhouette with cosine distance, inertia, average variance) (default=s)')
    parser.add_argument('--selec', default='bin', choices=['bin', 'rou', 'tour', 'rnd'], help='Selection Heuristic: bin | rou | tour | rnd (binary, roulette, tournament, random) (default=bin)')
    parser.add_argument('--ngen', type=int, default=300, help='Number of generations (default=100)')
    parser.add_argument('--max_no_improv', '-mximp', type=float, default=0.2, help='Percentage of generations with no improvement to force GA to stop (default=0.2)')
    parser.add_argument('--pop', type=int, default=30, help='Population size (default=30)')
    parser.add_argument('--cxpb', type=float, default=0.8, help='Initial crossover probability (default=0.8)')
    parser.add_argument('--mincxpb', type=float, default=0.1, help='Minimum crossover probability (default=0.1)')
    parser.add_argument('--mutpb', type=float, default=0.01, help='Mutation probability (default=0.01)')
    parser.add_argument('--elsize', default=0.05, type=float, help='Percentage of population to keep in the elite (default=0.05)')
    parser.add_argument('--mins', type=int, default=3, help='Minimum size of solution (default=3)')
    parser.add_argument('--maxs', type=int, default=6, help='Maximum size of solution (default=6)')
    parser.add_argument('--corr_threshold', '-crth', type=float, default=0.75, help='Value for correlation threshold (absolute value). Used to create restrictions (default=0.75)')
    parser.add_argument('--divfac', type=float, default=0.1, help='Percentage of population to be diversified after max_no_improv/2 iterations without improve the best solution (default=0.1)')
    parser.add_argument('--divstep', type=float, default=0.1, help='Percentage of generations with no improvement to force diversification (should be less than max_no_improv (default=0.1)')
    parser.add_argument('--toursize', type=float, default=0.2, help='Percentage of population to parcitipate of tournament selection (default=0.2)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose excution of GA (default=False)')
    parser.add_argument('--wo', action='store_true', help='Data with outliers (defaut=False)')
    parser.add_argument('--pltvar', action='store_true', help='Plot variances (default=False)')
    parser.add_argument('--pltfile', help='File to save variance plot')
    args = parser.parse_args()
    
    max_no_improv = int(np.round(args.max_no_improv * args.ngen))
    divstep = int(np.round(args.divstep * args.ngen))
    
    ### Loading data
    if args.wo:
        data = read_data('df_data')
    else:
        data = read_data('df_data_pruned')
        
    ### Normalizing data
    for col in data.columns:
        data[col] = (data[col] - data[col].min()) / (data[col].max() - data[col].min())
        
    ### Instantiate the problem
    if args.metric == 'v':
        maximise = True
        problem = VarianceProblem(data,
                                  args.mins,
                                  args.maxs,
                                  args.corr_threshold,
                                  maximise=maximise)
    elif args.metric == 'se':
        maximise = True
        problem = ClusteringProblem(args.k,
                                    'silhouette-euclidean',
                                    args.seed,
                                    data,
                                    args.mins,
                                    args.maxs,
                                    args.corr_threshold,
                                    maximise=maximise)
    elif args.metric == 'sc':
        maximise = True
        problem = ClusteringProblem(args.k,
                                    'silhouette-cosine',
                                    args.seed,
                                    data,
                                    args.mins,
                                    args.maxs,
                                    args.corr_threshold,
                                    maximise=maximise)
    else:
        maximise = False
        problem = ClusteringProblem(args.k,
                                    'inertia',
                                    args.seed,
                                    data,
                                    args.mins,
                                    args.maxs,
                                    args.corr_threshold,
                                    maximise=maximise)

    ### Setting up genetic algorithm
    genetic = GeneticAlgorithm(data,
                               population_size=args.pop,
                               generations=args.ngen,
                               crossover_probability=args.cxpb,
                               mutation_probability=args.mutpb,
                               elitism=args.elsize,
                               maximise_fitness=maximise,
                               max_no_improv=max_no_improv,
                               verbose=args.verbose,
                               min_crossover_probability=args.mincxpb,
                               diversification_factor=args.divfac,
                               diversification_step=divstep)
    
    genetic.fitness_function = problem.fitness
    genetic.create_individual = problem.create_individual
    genetic.mutate_function = problem.mutate
    genetic.crossover_function = problem.crossover
    if args.selec == 'bin':
        genetic.selection_function = problem.binary_selection
    elif args.selec == 'rou':
        genetic.selection_function = problem.roulette_selection
    elif args.selec == 'rnd':
        genetic.selection_function = genetic.random_selection
    # If none of the above options, leaves the default selection: tournament
    
    ### Executing GA
    start_time = time.time()
    max_gen_reached = genetic.run()
    elapsed_time = time.time() - start_time
    
    ### Show and save results
    print('\nLast generation:')
    for i,ind in enumerate(genetic.last_generation()):
        print('%d -> ' % i, end='')
        print_solution(ind, data)
        
    print('\nBest', end=' ')
    print_solution(genetic.best_individual(), data)
    
    print('\nTotal elapsed time: %s' % (get_formatted_time(elapsed_time)))
    
    if not max_gen_reached:
        print('\nStopped after %d generations without improvement.\n' % max_no_improv)
    
    if args.metric == 'v':
        if args.pltfile:
            problem.plot_variances(show=args.pltvar, save_file=args.pltfile)
        elif args.pltvar:
            problem.plot_variances(show=args.pltvar)
        
    save_solution(genetic.last_generation(), data, elapsed_time, max_no_improv, max_gen_reached, args)

if __name__ == '__main__':
    main()
