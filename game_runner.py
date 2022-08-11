from uuid import uuid4
from elements.mlp import MLP
from elements.player.player_mlp_bot import PlayerMLPBot
from evolution_machine import EvolutionMachine
from game import Game


class GameRunner:
    # Module used for running and tracking multiple runs of the Qwixx game

    def __init__(
        self,
        evolution_machine,
        population_size,
        n_generations,
        random_init,
        event_handler,
    ):
        self.evolution_machine = evolution_machine
        self.population_size = population_size
        self.n_generations = n_generations
        self.random_init = random_init
        self.event_handler = event_handler

    def run(self):
        population = self.create_initial_population(
            self.population_size, self.random_init, self.event_handler
        )

        for generation in range(self.n_generations):
            # Run the game to determine fitness
            population_fitness = self.play_population_1_v_1(
                population, games_per_pair=1
            )

            # Rank the players and get their chromosomes
            ranked_population = self.rank_population_on_fitness(population_fitness)
            ranked_chromosomes = self.chromosomes_from_population(
                list(zip(*ranked_population))[0]
            )

            print(
                f"Generation {generation}, best fitness = {max(population_fitness.values())}, mean fitness = {sum(population_fitness.values()) / len(population_fitness)}"
            )

            # Get a new population of chromosomes and turn them into players for the next generation
            new_population_chromosomes = self.evolution_machine.evolution_step(
                ranked_chromosomes
            )
            population = self.create_population_from_chromosomes(
                new_population_chromosomes, self.event_handler
            )

    def create_initial_population(self, population_size, random_flag, event_handler):
        population = []
        for _ in range(population_size):
            population.append(
                PlayerMLPBot(
                    uuid4(),
                    event_handler,
                    MLP(
                        n_input=14,
                        n_hidden=10,
                        n_output=1,
                        random_initialization=random_flag,
                    ),
                )
            )
        return population

    def create_population_from_chromosomes(self, chromosomes, event_handler):
        population = []
        for chromosome in chromosomes:
            population.append(
                PlayerMLPBot(
                    uuid4(),
                    event_handler,
                    MLP(n_input=14, n_hidden=10, n_output=1, chromosome=chromosome),
                )
            )
        return population

    def play_population_1_v_1(self, population, games_per_pair=1):
        population_fitness = {player: 0 for player in population}
        for player_1 in population:
            for player_2 in population:
                if player_1 == player_2:
                    continue
                for _ in range(games_per_pair):
                    game = Game([player_1, player_2])
                    game.play()
                    population_fitness[player_1] += self.calculate_fitness(player_1)
                    population_fitness[player_2] += self.calculate_fitness(player_2)
                    player_1.new_score_card()
                    player_2.new_score_card()

        for player in population_fitness:
            population_fitness[player] = float(population_fitness[player]) / float(
                ((len(population) - 1) * games_per_pair)
            )
        return population_fitness

    def rank_population_on_fitness(self, population_fitness):
        ranked_population = sorted(
            population_fitness.items(), key=lambda kv: kv[1], reverse=True
        )
        return ranked_population

    def chromosomes_from_population(self, population):
        chromosome_population = [player.mlp.chromosome for player in population]
        return chromosome_population

    def calculate_fitness(self, player):
        return player.score_card.score["Total"]

    # init 50 agents with chromosomes
    # all agents play each other n times e.g. 50*50*4 = 10000 games per generation
    # calculate fitness for each agent -- average score (perhaps with a win factor included, e.g. fitness = 0.8 * avg_score + 0.2 * win_bonus)
    # rank agents on fitness (here print average fitness and top fitness to track progress)
    # get chromosomes from agents, send them to the evolution machine and receive a new set of chromosomes
    # repeat for g generations

    # todo -- have player act with mlp to decide
    # board to mlp input
