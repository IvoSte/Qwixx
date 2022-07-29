from elements.player import Player
from game import Game
from eventHandler import EventHandler
import pandas as pd

from statistics import Statistics


def main():

    n_games = 1000
    event_handler = EventHandler()
    players = [Player("Ivo", event_handler, white_die_tolerance=2, colored_die_tolerance=2), \
            Player("Elrón", event_handler, white_die_tolerance=1, colored_die_tolerance=1)]

    results = run_game_n_times(n_games, players)
    stats = Statistics(results, n_games, len(players))
    stats.quick_analysis()


def run_game(players):
    game = Game(players)
    game.play()

def run_game_n_times(n, players):
    df = pd.DataFrame(columns= ['Game #', 'Player name', 'Ranking', 'Draw?', 'Points', 'Marks', 'Failed Throws', 'Rows Locked'])
    for i in range(n):
        game = Game(players)
        game.play()
        results = game.get_results()
        for result in results:
            result['Game #'] = i
            df = pd.concat([df,pd.Series(result).to_frame().T], axis = 0)
    return df


if __name__ == "__main__":
    main()

# Notes to do
# -- Players lock the lock even if they were not at turn
# -- Player now always takes the colored die throw, it should be able to refuse if it took the white one

# -- Player inputs
# -- easier inputs / game analysis to train algorithms on / monte carlo simulation
# Misschien leuk om ipv RL moeilijk te doen, gewoon ff de game tantoe vaak runnen met simpele regels voor strategieen
# En dan kijken welke het meest succesvol is (-- bv altijd hitten op < 2)