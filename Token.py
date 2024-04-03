from enum import Enum


class Token(Enum):
    EMPTY = ' '
    RED = 'R'
    YELLOW = 'Y'

    def __str__(self):
        return self.value
