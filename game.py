from dataclasses import dataclass
from elements.dice import Dice
from elements.score_card import ScoreCard

@dataclass
class Move:
    value: int
    color: str

class Game:

    def __init__(self, players):
        self.dice = [
            Dice("WHITE", 6), 
            Dice("WHITE", 6), 
            Dice("RED", 6), 
            Dice("YELLOW", 6), 
            Dice("GREEN", 6), 
            Dice("BLUE", 6)
        ]
        self.row_closed = {
            "RED" : False,
            "YELLOW" : False,
            "GREEN" : False,
            "BLUE" : False,
        }
        self.current_die_throw = []
        self.dice_throw_sums = []

        self.players = players

        self.player_at_turn = None

        self.round_counter = 0
        self.game_finished = False

    def play(self):
        while self.game_finished == False:
            self.round()

            self.round_counter += 1
            if self.round_counter > 100:
                self.game_finished = True
        self.finish_game()

    def round(self):
        self.manage_turns()

        self.throw_dice()
        
        self.calculate_dice_throw_sums()

        self.notify_all_players_of_white_throw()

        self.check_game_over()

        self.notify_player_at_turn_of_colored_throws()

        self.check_game_over()

    def manage_turns(self):
        self.players.append(self.players.pop(0))
        self.player_at_turn = self.players[0]
        print(f"{self.player_at_turn.name}'s turn!")

    def throw_dice(self):
        self.current_die_throw = []
        print("Throwing dice!")
        for die in self.dice:
            die_throw = die.throw()
            self.current_die_throw.append(die_throw)
            print(f"{die_throw.color} = {die_throw.value}")

    def calculate_dice_throw_sums(self):
        self.dice_throw_sums = []
        white_dice_throws = [die_throw for die_throw in self.current_die_throw if die_throw.color == "WHITE"]
        color_dice_throws = [die_throw for die_throw in self.current_die_throw if die_throw.color != "WHITE"]
        
        self.dice_throw_sums.append(Move(sum([throw.value for throw in white_dice_throws]), "WHITE"))

        for white_die_throw in white_dice_throws:
            for color_die_throw in color_dice_throws:
                self.dice_throw_sums.append(Move(white_die_throw.value + color_die_throw.value, color_die_throw.color))

    def notify_all_players_of_white_throw(self):
        for player in self.players:
            player.notify_white_throw(self.dice_throw_sums[0])

    def notify_player_at_turn_of_colored_throws(self):
        self.player_at_turn.notify_colored_throw(self.dice_throw_sums[1:len(self.dice_throw_sums) + 1])

    def check_game_over(self):
        # Two conditions for the game to end: either two rows are locked, or one player has four failed throws
        row_closed_count = 0
        for player in self.players:
            for locked in player.score_card.row_locks.values():
                if locked:
                    row_closed_count += 1
        if row_closed_count >= 2:
            print("Game ended! Two rows locked.")
            self.game_finished = True
            return

        for player in self.players:
            if player.score_card.check_four_failed_throws():
                print(f"Game ended! Four failed throws by {player.name}!")
                self.game_finished = True

    def finish_game(self):
        for player in self.players:
            print()
            player.score_card.calculate_score()
            player.report()

        ranked_players = sorted(self.players, key=lambda x: x.score_card.score["Total"], reverse = True)
        print()
        print(f"{ranked_players[0].name} is the winner!!")
        print(f"{ranked_players[-1].name} is the loser (en een nerd).")
