from dataclasses import dataclass
from elements.score_card import ScoreCard
from game import Move

@dataclass
class MoveEvaluation:
    move: Move
    evaluation: int

class Player:

    def __init__(self, name, event_handler):
        self.name = name
        self.score_card = ScoreCard(event_handler)
        self.white_die_tolerance = 2
        self.colored_die_tolerance = 2
        self.played_white_this_turn = False

    def notify_white_throw(self, move):
        # notify a player on the white dice thrown, player can opt to mark any of its rows with the value
        #print(f"{self.name} evaluates the white dice throw...")

        # Check possible moves
        possible_moves = self.filter_impossible_moves([Move(move.value, "RED"), Move(move.value, "YELLOW"), Move(move.value, "GREEN"), Move(move.value, "BLUE")])
        #print(f"{possible_moves = }")

        if len(possible_moves) == 0:
            print(f"{self.name} skips the white dice throw because no move is available.")
            return
        # Evaluate and rank possible moves
        ranked_moves = self.rank_possible_moves(possible_moves)

        # If rank evaluation within tolerance, play the move
        if ranked_moves[0].evaluation <= self.white_die_tolerance:
            print(f"{self.name} takes the {move.value} white dice throw.")
            self.play_move(ranked_moves[0].move)
            self.played_white_this_turn = True
        else:
            print(f"{self.name} skips the white dice throw.")
            self.played_white_this_turn = False

    def notify_colored_throw(self, moves):
        #print(f"{self.name} evaluates the colored dice throw...")

        # Check possible moves
        possible_moves = self.filter_impossible_moves(moves)

        # If there are no possible moves, play a failed throw
        if len(possible_moves) == 0:
            if not self.played_white_this_turn:
                self.play_failed_throw()
            return

        # Evaluate and rank possible moves
        ranked_moves = self.rank_possible_moves(possible_moves)

        # If the move is not within tolerance and player already played a move
        if ranked_moves[0].evaluation > self.colored_die_tolerance and self.played_white_this_turn:
            # the player opts to skip the colored throw
            return
        # Play best move
        self.play_move(ranked_moves[0].move)

    def filter_impossible_moves(self, moves):
        possible_moves = []
        for move in moves:
            if self.score_card.check_if_mark_is_possible(move.color, move.value):
                possible_moves.append(move)
        return possible_moves

    def rank_possible_moves(self, possible_moves):
        ranked_moves = []
        for move in possible_moves:
            ranked_moves.append(self.evaluate_move(move))
        ranked_moves = sorted(ranked_moves, key=lambda x: x.evaluation)
        return ranked_moves

    def evaluate_move(self, move):
        """ This function can be extended a lot, e.g. by knowing that making the last move closes the row, knowing how far the game is progressed etc."""
        return MoveEvaluation(move, self.score_card.distance_to_next_mark(move.color, move.value))

    def play_move(self, move):
        print(f"{self.name} marks {move.value} for {move.color}.")
        self.score_card.mark_card_value(move.color, move.value)

    def play_failed_throw(self):
        print(f"{self.name} has a failed throw!.")
        self.score_card.mark_failed_throw()

    def report(self):
        print(f"{self.name}'s final score card:")
        self.score_card.report()