
from dataclasses import dataclass
from colorama import Fore, Back, Style

from eventHandler import RowClosedEvent


@dataclass
class CardValue:
    value: int
    marked: bool

class ScoreCard:

    def __init__(self, event_handler):
        self.event_handler = event_handler
        self.event_handler.register_listener(self)

        self.rows = {
            "RED" : [CardValue(value, False) for value in range(2,13)],
            "YELLOW" : [CardValue(value, False) for value in range(2,13)],
            "GREEN" : [CardValue(value, False) for value in range(12,1,-1)],
            "BLUE" : [CardValue(value, False) for value in range(12,1,-1)],
        }
        self.row_locks = {
            "RED" : False,
            "YELLOW" : False,
            "GREEN" : False,
            "BLUE" : False,
        }
        self.row_closed = {
            "RED" : False,
            "YELLOW" : False,
            "GREEN" : False,
            "BLUE" : False,
        }
        self.failed_throw = [False, False, False, False]
        self.score_mapping = {
            0 : 0,
            1 : 1,
            2 : 3,
            3 : 6,
            4 : 10,
            5 : 15,
            6 : 21,
            7 : 28,
            8 : 36,
            9 : 45,
            10 : 55,
            11 : 66,
            12 : 78,
        }
        self.score = {
            "RED" : 0,
            "YELLOW" : 0,
            "GREEN" : 0,
            "BLUE" : 0,
            "Failed" : 0,
            "Total" : 0
        }

    def notify(self, event):
        if isinstance(event, RowClosedEvent):
            self.close_row(RowClosedEvent.color)

    def mark_card_value(self, color, value):
        """ Mark off a value from a row if that move is possible. 
            If any score after this one is marked, this one can't be marked anymore."""
        for idx, row_value in enumerate(reversed(self.rows[color])):
            if row_value.marked:
                print("Invalid Action")
                return
            if row_value.value == value and not self.row_closed[color]:
                row_value.marked = True
                if idx == 0:
                    self.lock_row(color)
                return

    def lock_row(self, color):
        self.row_locks[color] = True
        self.event_handler.post(RowClosedEvent(color = color))

    def close_row(self, color):
        self.row_closed[color] = True

    def mark_failed_throw(self):
        for idx, value in enumerate(self.failed_throw):
            if not value:
                self.failed_throw[idx] = True
                return

    def count_failed_throws(self):
        count = 0
        for check in self.failed_throw:
            if check:
                count += 1
        return count


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
        self.score["Total"] = self.score["RED"] + self.score["YELLOW"] + self.score["GREEN"] \
                            + self.score["BLUE"] + self.score["Failed"]

    def count_row_marks(self, color):
        count = sum(value.marked == True for value in self.rows[color])
        if self.row_locks[color] == True:
            count += 1
        return count

    def __str__(self):
        s = ""
        for key, value in self.rows.items():
            s += (f"{key} row : {value}\n")
        return s

    def print_card(self):
        self.print_row(Back.RED, self.rows["RED"], self.row_locks["RED"])
        self.print_row(Back.YELLOW, self.rows["YELLOW"], self.row_locks["YELLOW"])
        self.print_row(Back.GREEN, self.rows["GREEN"], self.row_locks["GREEN"])
        self.print_row(Back.CYAN, self.rows["BLUE"], self.row_locks["BLUE"])

    def print_row(self, print_color, row, locked):
        print(f"{print_color} > ", end = '')
        for card_value in row:
            color = Back.WHITE if card_value.marked else print_color
            print(f"{color}{card_value.value}{print_color}", end = ' ')
        color = Back.WHITE if locked else print_color
        print(f"{color}L{print_color}", end = '')
        print(f"{Style.RESET_ALL}")

    def report(self):
        print("Card")
        self.print_card()
        print("Score")
        print(self.score)

if __name__ == "__main__":
    sc = ScoreCard()
    print(sc)