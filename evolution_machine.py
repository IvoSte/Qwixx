from math import ceil
import random


class EvolutionMachine:

    def __init__(self, reproduce_fraction, cull_fraction, mutation_probability, mutation_range):
        self.reproduce_fraction = reproduce_fraction
        self.cull_fraction = cull_fraction

        self.mutation_probability = mutation_probability
        self.mutation_range = mutation_range

    def evolution_step(self, ranked_population):
        # get the number of individuals to reproduce and cull
        n_reproduce = ceil(self.reproduce_fraction * len(ranked_population))
        n_cull = ceil(self.cull_fraction * len(ranked_population))

        # Make sure they are even amounts
        n_reproduce = n_reproduce if n_reproduce % 2 == 0 else n_reproduce + 1
        n_cull = n_cull if n_cull % 2 == 0 else n_cull + 1

        # Cull bottom percentage
        new_population = self.cull_population(ranked_population, n_cull)

        # Produce offspring
        new_population = self.reproduce_population(new_population, n_reproduce)

    def cull_population(self, population, n_cull):
        return population[0:len(population) - n_cull]

    def reproduce_population(self, population, n_reproduce):
        # get random pairings
        parents = population[0:n_reproduce]
        random.shuffle(parents)
        offspring = []
        for idx in range(len(parents)/2):
            offspring += self.crossover(parents[idx], parents[idx + 1])
        for child in offspring:
            child = self.mutate_chromosome(child, self.mutation_probability, self.mutation_range)
        population += offspring
        return population

    def crossover(self, parent_1, parent_2):
        # Produce two offsprings based on two parents, both getting the other gene of the parents.
        assert len(parent_1) == len(parent_2), f"Length of parent chromosomes unequal at crossover step."
        offspring_1 = []
        offspring_2 = []
        for idx in range(len(parent_1)):
            if random.random() < 0.5:
                offspring_1.insert(idx, parent_1[idx])
                offspring_2.insert(idx, parent_2[idx])
            else:
                offspring_1.insert(idx, parent_2[idx])
                offspring_2.insert(idx, parent_1[idx])

        return [offspring_1, offspring_2]

    def mutate_chromosome(self, chromosome, mutation_probability, mutation_range):
        # The mutation probability counts for each gene, so we can mutate multiple genes on the same chromosome the same time if we wish.
        for idx in range(len(chromosome)):
            if random.random() < mutation_probability:
                mutation_step = random.uniform(-1* mutation_range, mutation_range)
                chromosome[idx] += mutation_step

        return chromosome