from enum import IntEnum

BOARD_SIZE = 3


class Role(IntEnum):
    USER = 1
    BOT = 2


class TicTacToeArgs(IntEnum):
    EMPTY = -1
    O = 0  # noqa
    X = 1  # noqa
