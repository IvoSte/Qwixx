import logging
from elements.player.player import MoveEvaluation, MoveState, Player
from game import Move


class PlayerMLPBot(Player):
    def __init__(self, name, event_handler, mlp):
        Player.__init__(self, name, event_handler)
        self.mlp = mlp

        # Evaluations of moves are between 0-1.
        # To decide if the best move is good enough to play,
        # see if the confidence of the move is within threshold
        # These values should not be changed between training and testing, as the MLP
        # Optimizes for these values
        # Possibly design a better system (as colored certainty should differ when a move is already made)
        self.white_certainty_threshold = 0.8
        self.colored_certainty_threshold = 0.5

    def evaluate_white_throw(self, move):
        # Check possible moves
        possible_moves = self.filter_impossible_moves(
            [
                Move(move.value, "RED"),
                Move(move.value, "YELLOW"),
                Move(move.value, "GREEN"),
                Move(move.value, "BLUE"),
            ]
        )

        if len(possible_moves) == 0:
            logging.info(
                f"{self.name} skips the white dice throw because no move is available."
            )
            return
        # Evaluate and rank possible moves
        ranked_moves = self.rank_possible_moves(possible_moves)

        # If rank evaluation within tolerance, play the move
        if ranked_moves[0].evaluation <= self.white_certainty_threshold:
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
        if (
            ranked_moves[0].evaluation > self.colored_certainty_threshold
            and self.played_white_this_turn
        ):
            # the player opts to skip the colored throw
            return
        # Play best move
        self.play_move(ranked_moves[0].move)

    def evaluate_move(self, move):
        return MoveEvaluation(move, self.evaluate_move_with_mlp(move))

    def evaluate_move_with_mlp(self, move):
        move_state = MoveState().from_move(move)
        card_state = self.score_card.get_card_state()

        mlp_input = move_state.to_list() + card_state.to_list()
        return self.mlp.evaluate_input(mlp_input)
