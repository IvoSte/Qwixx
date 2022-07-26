from dataclasses import dataclass
from colorama import Fore, Back, Style

from eventHandler import RowClosedEvent


@dataclass
class CardValue:
    value: int
    marked: bool


@dataclass
class CardState:
    red_marks: int
    red_next_value: int
    yellow_marks: int
    yellow_next_value: int
    green_marks: int
    green_next_value: int
    blue_marks: int
    blue_next_value: int
    failed_throws: int

    def to_list(self):
        return [
            self.red_marks,
            self.red_next_value,
            self.yellow_marks,
            self.yellow_next_value,
            self.green_marks,
            self.green_next_value,
            self.blue_marks,
            self.blue_next_value,
            self.failed_throws,
        ]


class ScoreCard:
    def __init__(self, event_handler):
        self.event_handler = event_handler
        self.event_handler.register_listener(self)

        self.rows = {
            "RED": [CardValue(value, False) for value in range(2, 13)],
            "YELLOW": [CardValue(value, False) for value in range(2, 13)],
            "GREEN": [CardValue(value, False) for value in range(12, 1, -1)],
            "BLUE": [CardValue(value, False) for value in range(12, 1, -1)],
        }
        self.row_locks = {
            "RED": False,
            "YELLOW": False,
            "GREEN": False,
            "BLUE": False,
        }
        self.row_closed = {
            "RED": False,
            "YELLOW": False,
            "GREEN": False,
            "BLUE": False,
        }
        self.failed_throw = [False, False, False, False]
        self.score_mapping = {
            0: 0,
            1: 1,
            2: 3,
            3: 6,
            4: 10,
            5: 15,
            6: 21,
            7: 28,
            8: 36,
            9: 45,
            10: 55,
            11: 66,
            12: 78,
        }
        self.score = {
            "RED": 0,
            "YELLOW": 0,
            "GREEN": 0,
            "BLUE": 0,
            "Failed": 0,
            "Total": 0,
        }

    def notify(self, event):
        if isinstance(event, RowClosedEvent):
            self.close_row(RowClosedEvent.color)

    def mark_card_value(self, color, value):
        """Mark off a value from a row if that move is possible.
        If any score after this one is marked, this one can't be marked anymore."""
        for idx, row_value in enumerate(reversed(self.rows[color])):
            if row_value.marked:
                print("Invalid Action")
                return
            if row_value.value == value and not self.row_closed[color]:
                row_value.marked = True
                # Final mark needs to lock the row, but can only be placed if 5 or more marks have been set in this row.
                if idx == 0:
                    if self.count_row_marks(color) >= 5:
                        self.lock_row(color)
                    else:
                        row_value.marked = False
                return

    def lock_row(self, color):
        self.row_locks[color] = True
        self.event_handler.post(RowClosedEvent(color=color))

    def close_row(self, color):
        self.row_closed[color] = True

    def mark_failed_throw(self):
        for idx, value in enumerate(self.failed_throw):
            if not value:
                self.failed_throw[idx] = True
                return

    def count_failed_throws(self):
        return sum(self.failed_throw)

    def check_four_failed_throws(self):
        return self.count_failed_throws() == 4

    def check_if_mark_is_possible(self, color, value) -> bool:
        if self.row_closed[color]:
            return False

        for row_value in reversed(self.rows[color]):
            if row_value.marked:
                return False
            if row_value.value == value:
                return True

    def distance_to_next_mark(self, color, value) -> int:
        counter = 0
        counting = False
        for row_value in reversed(self.rows[color]):
            if row_value.marked:
                return counter
            if counting:
                counter += 1
            if row_value.value == value:
                counting = True
        return counter

    def first_open_row_value(self, color) -> int:
        # grab the last value
        value = self.rows[color][len(self.rows[color]) - 1].value
        for row_value in reversed(self.rows[color]):
            # if the value is marked, return the previous value of the row
            if row_value.marked:
                return value
            value = row_value.value
        return value

    def calculate_score(self):
        self.calculate_row_score("RED")
        self.calculate_row_score("YELLOW")
        self.calculate_row_score("GREEN")
        self.calculate_row_score("BLUE")
        self.calculate_failed_throw_score()
        self.calculate_total_score()

    def calculate_row_score(self, color):
        self.score[color] = self.score_mapping[self.count_row_marks(color)]

    def calculate_failed_throw_score(self):
        self.score["Failed"] = self.count_failed_throws() * -5

    def calculate_total_score(self):
        self.score["Total"] = (
            self.score["RED"]
            + self.score["YELLOW"]
            + self.score["GREEN"]
            + self.score["BLUE"]
            + self.score["Failed"]
        )

    def count_row_marks(self, color):
        count = sum(value.marked == True for value in self.rows[color])
        if self.row_locks[color] == True:
            count += 1
        return count

    def count_total_marks(self):
        total = 0
        total += self.count_row_marks("RED")
        total += self.count_row_marks("YELLOW")
        total += self.count_row_marks("GREEN")
        total += self.count_row_marks("BLUE")
        return total

    def count_row_locks(self):
        return sum(self.row_locks.values())

    def get_card_state(self):
        state = CardState(
            red_marks=self.count_row_marks("RED"),
            red_next_value=self.first_open_row_value("RED"),
            yellow_marks=self.count_row_marks("YELLOW"),
            yellow_next_value=self.first_open_row_value("YELLOW"),
            green_marks=self.count_row_marks("GREEN"),
            green_next_value=self.first_open_row_value("GREEN"),
            blue_marks=self.count_row_marks("BLUE"),
            blue_next_value=self.first_open_row_value("BLUE"),
            failed_throws=self.count_failed_throws(),
        )
        return state

    def __str__(self):
        s = ""
        for key, value in self.rows.items():
            s += f"{key} row : {value}\n"
        return s

    def print_card(self):
        self.print_row(Back.RED, self.rows["RED"], self.row_locks["RED"])
        self.print_row(Back.YELLOW, self.rows["YELLOW"], self.row_locks["YELLOW"])
        self.print_row(Back.GREEN, self.rows["GREEN"], self.row_locks["GREEN"])
        self.print_row(Back.CYAN, self.rows["BLUE"], self.row_locks["BLUE"])

    def print_row(self, print_color, row, locked):
        print(f"{print_color} > ", end="")
        for card_value in row:
            color = Back.WHITE if card_value.marked else print_color
            print(f"{color}{card_value.value}{print_color}", end=" ")
        color = Back.WHITE if locked else print_color
        print(f"{color}L{print_color}", end="")
        print(f"{Style.RESET_ALL}")

    def report(self):
        print("Card")
        self.print_card()
        print("Score")
        print(self.score)


if __name__ == "__main__":
    sc = ScoreCard()
    print(sc)
