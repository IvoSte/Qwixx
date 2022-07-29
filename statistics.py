

from unittest import result


class Statistics:

    def __init__(self, results, n_games, n_players):
        self.df = results
        self.n_games = n_games
        self.n_players = n_players
        self.player_names = self.df["Player name"].unique()

    def quick_analysis(self):
        player_wins = {} 
        for name in self.player_names:
            try: 
                player_wins[name] = self.df.loc[self.df['Player name'] == name]['Ranking'].value_counts()[1]
            except KeyError:
                player_wins[name] = 0

        print(f"Draws: {self.df['Draw?'].value_counts()[True]//len(self.player_names)}")

        print(f"Player wins: {player_wins}")

        print(f"Average rank: {self.mean_value_of_column_per_player('Ranking')}")

        print(f"Average failed throws: {self.mean_value_of_column_per_player('Failed Throws')}")

        print(f"Average rows locked: {self.mean_value_of_column_per_player('Rows Locked')}")

        print(f"Average points: {self.mean_value_of_column_per_player('Points')}")

        print(f"Average marks: {self.mean_value_of_column_per_player('Marks')}")

    def mean_value_of_column_per_player(self, column):
        return {name: self.df.loc[self.df['Player name'] == name][column].mean() for name in self.player_names}