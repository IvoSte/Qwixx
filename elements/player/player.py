from dataclasses import dataclass
from elements.score_card import ScoreCard
from game import Move
import logging


@dataclass
class MoveEvaluation:
    move: Move
    evaluation: int


@dataclass
class MoveState:
    value: int = 0
    red: bool = False
    yellow: bool = False
    green: bool = False
    blue: bool = False

    def to_list(self):
        return [
            self.value,
            int(self.red),
            int(self.yellow),
            int(self.green),
            int(self.blue),
        ]

    def from_move(self, move):
        return MoveState(
            move.value,
            move.color == "RED",
            move.color == "YELLOW",
            move.color == "GREEN",
            move.color == "BLUE",
        )


class Player:
    def __init__(self, name, event_handler):
        self.name = name
        self.event_handler = event_handler
        self.score_card = ScoreCard(event_handler)
        self.played_white_this_turn = False

    def new_score_card(self):
        self.score_card = ScoreCard(self.event_handler)

    def evaluate_white_throw(self, move):
        # notify a player on the white dice thrown, player can opt to mark any of its rows with the value
        logging.error(
            "Called function evaluate_white_throw() of base class Player, which should be overwritten by the behaviour of a subclass."
        )

    def evaluate_colored_throw(self, moves):
        logging.error(
            "Called function evaluate_colored_throw() of base class Player, which should be overwritten by the behaviour of a subclass."
        )

    def evaluate_move(self, move):
        """This function can be extended a lot, e.g. by knowing that making the last move closes the row, knowing how far the game is progressed etc."""
        logging.error(
            "Called function evaluate_move() of base class Player, which should be overwritten by the behaviour of a subclass."
        )
        return None

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

    def play_move(self, move):
        logging.info(f"{self.name} marks {move.value} for {move.color}.")
        self.score_card.mark_card_value(move.color, move.value)

    def play_failed_throw(self):
        logging.info(f"{self.name} has a failed throw!.")
        self.score_card.mark_failed_throw()

    def report(self):
        logging.info(f"{self.name}'s final score card:")
        self.score_card.report()

    def get_final_results(self):
        player_result = {
            "Player name": self.name,
            "Points": self.score_card.score["Total"],
            "Marks": self.score_card.count_total_marks(),
            "Failed Throws": self.score_card.score["Failed"] // 5,
            "Rows Locked": self.score_card.count_row_locks(),
        }
        return player_result
