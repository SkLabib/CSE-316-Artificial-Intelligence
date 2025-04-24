
import random

class Individual:
    def __init__(self, size):
        self.size = size
        self.genes = [random.randint(0, size - 1) for _ in range(size)]  # One queen per row, gene = column
        self.fitness = 0
        self.calc_fitness()

    def calc_fitness(self):
       
        non_attacking = 0
        total_pairs = self.size * (self.size - 1) // 2
        for i in range(self.size):
            for j in range(i + 1, self.size):
                if self.genes[i] != self.genes[j] and abs(self.genes[i] - self.genes[j]) != abs(i - j):
                    non_attacking += 1
        self.fitness = non_attacking

class Population:
    def __init__(self, size, n_queens):
        self.size = size
        self.individuals = [Individual(n_queens) for _ in range(size)]
        self.fittest = 0

    def calculate_fitness(self):
        for individual in self.individuals:
            individual.calc_fitness()
        self.get_fittest()

    def get_fittest(self):
        self.fittest = max(self.individuals, key=lambda x: x.fitness).fitness
        return max(self.individuals, key=lambda x: x.fitness)

    def get_second_fittest(self):
        sorted_individuals = sorted(self.individuals, key=lambda x: x.fitness, reverse=True)
        return sorted_individuals[1]

    def get_least_fittest_index(self):
        return min(range(self.size), key=lambda i: self.individuals[i].fitness)

class GeneticAlgorithm:
    def __init__(self, n_queens=8, population_size=100):
        self.n_queens = n_queens
        self.population = Population(population_size, n_queens)
        self.fittest = None
        self.second_fittest = None
        self.generation = 0

    def selection(self):
        self.fittest = self.population.get_fittest()
        self.second_fittest = self.population.get_second_fittest()

    def crossover(self):
        point = random.randint(0, self.n_queens - 1)
        for i in range(point):
            self.fittest.genes[i], self.second_fittest.genes[i] = self.second_fittest.genes[i], self.fittest.genes[i]

    def mutation(self):
        for individual in [self.fittest, self.second_fittest]:
            point = random.randint(0, self.n_queens - 1)
            individual.genes[point] = random.randint(0, self.n_queens - 1)

    def add_fittest_offspring(self):
        self.fittest.calc_fitness()
        self.second_fittest.calc_fitness()
        index = self.population.get_least_fittest_index()
        self.population.individuals[index] = max(self.fittest, self.second_fittest, key=lambda x: x.fitness)

    def run(self):
        self.population.calculate_fitness()
        print(f"Generation: {self.generation}, Fittest: {self.population.fittest}")
        max_fitness = self.n_queens * (self.n_queens - 1) // 2
        while self.population.fittest < max_fitness:
            self.generation += 1
            self.selection()
            self.crossover()
            if random.randint(0, 6) < 5:
                self.mutation()
            self.add_fittest_offspring()
            self.population.calculate_fitness()
            print(f"Generation: {self.generation}, Fittest: {self.population.fittest}")

        solution = self.population.get_fittest()
        print(f"\nSolution found in generation {self.generation}")
        print(f"Fitness: {solution.fitness}")
        print("Board Configuration:")
        self.print_board(solution.genes)

    def print_board(self, genes):
        for row in range(self.n_queens):
            line = ["Q" if genes[row] == col else "." for col in range(self.n_queens)]
            print(" ".join(line))


if __name__ == '__main__':
    ga = GeneticAlgorithm(n_queens=8, population_size=100)
    ga.run()
