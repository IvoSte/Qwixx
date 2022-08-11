from random import random
from elements.player.player import Player
from elements.player.player_simple_bot import PlayerSimpleBot
from evolution_machine import EvolutionMachine
from game import Game
from eventHandler import EventHandler
import pandas as pd

from statistics import Statistics

from game_runner import GameRunner

# Note: Something seems to be off with failed throws. Setting the tolerance to really high means a person will always take the dice if they can.
#       This should result in many failed throws, as the board leaves many gaps and little options. For some reason, the stat says otherwise.


def main():
    run_gamerunner()


def run_simple():
    n_games = 1000
    event_handler = EventHandler()
    players = [
        PlayerSimpleBot(
            "Ivo", event_handler, white_die_tolerance=2, colored_die_tolerance=2
        ),
        PlayerSimpleBot(
            "Elrón", event_handler, white_die_tolerance=1, colored_die_tolerance=1
        ),
    ]

    results = run_game_n_times(n_games, players)
    stats = Statistics(results, n_games, len(players))
    stats.quick_analysis()


def run_game(players):
    game = Game(players)
    game.play()


def run_game_n_times(n, players):
    df = pd.DataFrame(
        columns=[
            "Game #",
            "Player name",
            "Ranking",
            "Draw?",
            "Points",
            "Marks",
            "Failed Throws",
            "Rows Locked",
        ]
    )
    for i in range(n):
        game = Game(players)
        game.play()
        results = game.get_results()
        for result in results:
            result["Game #"] = i
            df = pd.concat([df, pd.Series(result).to_frame().T], axis=0)
    return df


def run_gamerunner():
    event_handler = EventHandler()
    evolution_machine = EvolutionMachine(
        reproduce_fraction=0.2,
        cull_fraction=0.2,
        mutation_probability=0.05,
        mutation_range=0.1,
    )
    game_runner = GameRunner(
        evolution_machine=evolution_machine,
        population_size=10,
        n_generations=10000,
        random_init=True,
        event_handler=event_handler,
    )
    game_runner.run()


if __name__ == "__main__":
    main()

# Notes to do
# -- Players lock the lock even if they were not at turn
# -- Player now always takes the colored die throw, it should be able to refuse if it took the white one

# -- Player inputs
# -- easier inputs / game analysis to train algorithms on / monte carlo simulation
# Misschien leuk om ipv RL moeilijk te doen, gewoon ff de game tantoe vaak runnen met simpele regels voor strategieen
# En dan kijken welke het meest succesvol is (-- bv altijd hitten op < 2)
