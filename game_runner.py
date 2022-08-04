


class GameRunner:
    # Module used for running and tracking multiple runs of the Qwixx game

    def __init__(self, game):
        self.game = game


    # init 50 agents with chromosomes
    # all agents play each other n times e.g. 50*50*4 = 10000 games per generation
    # calculate fitness for each agent -- average score (perhaps with a win factor included, e.g. fitness = 0.8 * avg_score + 0.2 * win_bonus)
    # rank agents on fitness (here print average fitness and top fitness to track progress)
    # get chromosomes from agents, send them to the evolution machine and receive a new set of chromosomes
    # repeat for g generations


    # todo -- have player act with mlp to decide 
    # board to mlp input