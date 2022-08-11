import logging
from elements.player.player import MoveEvaluation, Player
from game import Move


class PlayerSimpleBot(Player):

    def __init__(self, name, event_handler, white_die_tolerance = 2, colored_die_tolerance = 2):
        Player.__init__(self, name, event_handler)
        self.white_die_tolerance = white_die_tolerance
        self.colored_die_tolerance = colored_die_tolerance

    def evaluate_white_throw(self, move):
        # notify a player on the white dice thrown, player can opt to mark any of its rows with the value

        # Check possible moves
        possible_moves = self.filter_impossible_moves([Move(move.value, "RED"), Move(move.value, "YELLOW"), Move(move.value, "GREEN"), Move(move.value, "BLUE")])

        if len(possible_moves) == 0:
            logging.info(f"{self.name} skips the white dice throw because no move is available.")
            return
        # Evaluate and rank possible moves
        ranked_moves = self.rank_possible_moves(possible_moves)

        # If rank evaluation within tolerance, play the move
        if ranked_moves[0].evaluation <= self.white_die_tolerance:
            logging.info(f"{self.name} takes the {move.value} white dice throw.")
            self.play_move(ranked_moves[0].move)
            self.played_white_this_turn = True
        else:
            logging.info(f"{self.name} skips the white dice throw.")
            self.played_white_this_turn = False

    def evaluate_colored_throw(self, moves):
        # Evaluate the possible moves to make on a coloured throw and play the best move
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

    def evaluate_move(self, move):
        """ This function can be extended a lot, e.g. by knowing that making the last move closes the row, knowing how far the game is progressed etc."""
        return MoveEvaluation(move, self.score_card.distance_to_next_mark(move.color, move.value))
