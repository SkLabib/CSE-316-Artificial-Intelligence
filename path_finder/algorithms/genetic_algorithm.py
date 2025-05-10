import random
import time
import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms

class GeneticAlgorithm:
    def __init__(self, graph_builder, population_size=100, generations=100, 
                 crossover_prob=0.8, mutation_prob=0.2, elite_size=10):
        """Initialize the Genetic Algorithm for route optimization."""
        if graph_builder is None:
            raise ValueError("graph_builder must be provided!")
        if not hasattr(graph_builder, 'locations'):
            raise AttributeError("GraphBuilder missing 'locations' attribute.")
        
        self.graph_builder = graph_builder
        self.population_size = population_size
        self.generations = generations
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.elite_size = elite_size
        self.history = {'best': [], 'avg': []}
        
        # Set up DEAP genetic algorithm components
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # Minimization problem
        creator.create("Individual", list, fitness=creator.FitnessMin)
        
        self.toolbox = base.Toolbox()
        
        # Register functions for initialization and operations
        self._setup_toolbox()
    
    def _setup_toolbox(self):
        """Set up the genetic algorithm toolbox with operators."""
        # Register the permutation of indices as a representation of individuals
        n_locations = len(self.graph_builder.locations)
        
        # Create an individual as a randomly shuffled list of location indices
        self.toolbox.register("indices", random.sample, range(n_locations), n_locations)
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.toolbox.indices)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        
        # Register the evaluation function
        self.toolbox.register("evaluate", self._fitness_function)
        
        # Genetic operators
        self.toolbox.register("mate", tools.cxOrdered)  # Ordered crossover for permutations
        self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)  # Shuffle mutation
        self.toolbox.register("select", tools.selTournament, tournsize=3)  # Tournament selection
    
    def _fitness_function(self, individual):
        """Calculate the fitness of an individual (total route distance)."""
        total_distance = 0
        
        # Calculate the total distance of the route represented by the individual
        for i in range(len(individual) - 1):
            from_loc = individual[i]
            to_loc = individual[i + 1]
            total_distance += self.graph_builder.graph[from_loc][to_loc]['weight']
        
        # Add distance back to starting point if needed (TSP)
        # total_distance += self.graph_builder.graph[individual[-1]][individual[0]]['weight']
        
        return (total_distance,)  # Return as tuple for DEAP
    
    def optimize(self, start_time=None):
        """Run the genetic algorithm optimization."""
        start = time.time() if start_time is None else start_time
        
        # Reset history
        self.history = {'best': [], 'avg': []}
        
        # Initialize the population
        pop = self.toolbox.population(n=self.population_size)
        
        # Hall of Fame to keep track of the best individual
        hof = tools.HallOfFame(1)
        
        # Statistics to track progress
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("min", np.min)
        stats.register("max", np.max)
        
        # Run the algorithm
        pop, logbook = algorithms.eaSimple(
            pop, self.toolbox, 
            cxpb=self.crossover_prob, 
            mutpb=self.mutation_prob,
            ngen=self.generations,
            stats=stats,
            halloffame=hof,
            verbose=False
        )
        
        # Extract statistics for visualization
        for gen in range(self.generations + 1):
            if gen < len(logbook):
                self.history['best'].append(logbook[gen]['min'])
                self.history['avg'].append(logbook[gen]['avg'])
        
        best_individual = hof[0]
        best_fitness = best_individual.fitness.values[0]
        
        # Get the path and distance
        best_path = list(best_individual)
        best_distance = best_fitness
        
        # Calculate duration based on the best path
        best_duration = 0
        for i in range(len(best_path) - 1):
            from_loc = best_path[i]
            to_loc = best_path[i + 1]
            best_duration += self.graph_builder.graph[from_loc][to_loc]['duration']
        
        # Measure total runtime
        total_time = time.time() - start
        
        return {
            'algorithm': 'Genetic Algorithm',
            'path': best_path,
            'distance': best_distance,
            'duration': best_duration,
            'computation_time': total_time,
            'generations': self.generations,
            'population_size': self.population_size
        }
    
    def plot_evolution(self, figsize=(10, 6)):
        """Plot the evolution of the fitness over generations."""
        plt.figure(figsize=figsize)
        generations = range(len(self.history['best']))
        
        plt.plot(generations, self.history['best'], 'b-', label='Best Fitness')
        plt.plot(generations, self.history['avg'], 'r-', label='Average Fitness')
        
        plt.title('Genetic Algorithm Evolution')
        plt.xlabel('Generation')
        plt.ylabel('Fitness (Total Distance)')
        plt.legend()
        plt.grid(True)
        
        return plt.gcf() 