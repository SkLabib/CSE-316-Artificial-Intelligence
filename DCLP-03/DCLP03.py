import random

T = 7  
k = 2  
population_size = 10
generations = 100

def create_individual():
    return [random.randint(0, 9) for _ in range(k)]

def fitness(individual):
    return abs(T - sum(individual))

def mutate(individual):
    i = random.randint(0, k-1)
    individual[i] = random.randint(0, 9)
    return individual

population = [create_individual() for _ in range(population_size)]

for generation in range(generations):
    population.sort(key=fitness)

    if fitness(population[0]) == 0:
        break

    survivors = population[:population_size // 2]

    children = []
    while len(children) < population_size - len(survivors):
        parent = random.choice(survivors)
        child = mutate(parent.copy())
        children.append(child)

    population = survivors + children

print("Best solution:", population[0], "Sum:", sum(population[0]))
