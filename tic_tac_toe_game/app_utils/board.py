import copy
import random
import time
from functools import wraps

from tic_tac_toe_game import constants
from tic_tac_toe_game.app_utils import exceptions


def action_checks(action_func):
    @wraps(action_func)
    def wrapper(self, *args, **kwargs):
        if self.is_board_full():
            raise exceptions.BoardFullException()

        row, col = action_func(self, *args, **kwargs)

        if self.is_game_complete(row=row, col=col):
            raise exceptions.GameCompleteException()

    return wrapper


# NOTE Assume board size is 3x3 for now
class TicTacToeBoard:
    def __init__(self, start_role: int = constants.Role.USER) -> None:
        self.start_role = start_role
        # NOTE always have deep copy. Shallow copy will mess up the matrix
        row = [constants.TicTacToeArgs.EMPTY] * constants.BOARD_SIZE
        self.board = [copy.deepcopy(row) for _ in range(constants.BOARD_SIZE)]
        self.free_spaces = list(
            range(constants.BOARD_SIZE * constants.BOARD_SIZE)
        )

    def is_board_full(self):
        return len(self.free_spaces) == 0

    def is_game_complete(self, row: int, col: int) -> bool:
        check_row = map(lambda x: x == self.board[row][col], self.board[row])
        is_row_same = all(check_row)
        check_col = [
            self.board[i][col] == self.board[row][col]
            for i in range(constants.BOARD_SIZE)
        ]

        is_col_same = all(check_col)
        check_consecutive_marks = bool(is_row_same + is_col_same)

        if (row + col + 1) == constants.BOARD_SIZE:
            check_diag = [
                self.board[i][constants.BOARD_SIZE - 1 - i]
                == self.board[row][col]
                for i in range(constants.BOARD_SIZE)
            ]
            is_diag_same = all(check_diag)
            check_consecutive_marks = bool(
                check_consecutive_marks + is_diag_same
            )

        if row == col:
            check_diag = [
                self.board[i][i] == self.board[row][col]
                for i in range(constants.BOARD_SIZE)
            ]
            is_diag_same = all(check_diag)
            check_consecutive_marks = bool(
                check_consecutive_marks + is_diag_same
            )

        return check_consecutive_marks

    @action_checks
    def user_action(self, position: int):
        row = position // constants.BOARD_SIZE
        col = position % constants.BOARD_SIZE

        if position not in self.free_spaces:
            raise exceptions.PositionNotEmptyException()
        self.board[row][col] = (
            constants.TicTacToeArgs.X
            if self.start_role == constants.Role.USER
            else constants.TicTacToeArgs.O
        )
        self.free_spaces.remove(position)
        return row, col

    @action_checks
    def random_ai_action(self):
        choice = random.choice(self.free_spaces)

        row = choice // constants.BOARD_SIZE
        col = choice % constants.BOARD_SIZE

        self.board[row][col] = (
            constants.TicTacToeArgs.X
            if self.start_role == constants.Role.BOT
            else constants.TicTacToeArgs.O
        )
        self.free_spaces.remove(choice)
        return row, col

    def minimax_ai_action(self):
        raise NotImplementedError()

    def ml_ai_action(self):
        raise NotImplementedError()

    def show_board(self):
        for row in self.board:
            for element in row:
                print(f"{element:3}", end=" ")
            print()

    def play(self):
        while not self.is_board_full():
            print("Doing User Action....")
            position = int(input("Give us the position: ").strip())
            try:
                self.user_action(position=position)
            except exceptions.BoardFullException:
                print("Board is full...")
                self.show_board()
                break
            except exceptions.GameCompleteException:
                print("User wins!!!")
                self.show_board()
                break
            time.sleep(1)
            print("AI is thinking")
            time.sleep(3)
            print("Doing AI action")
            try:
                self.random_ai_action()
            except exceptions.BoardFullException:
                print("Board is full....")
                self.show_board()
                break
            except exceptions.GameCompleteException:
                print("Bot wins!!!")
                self.show_board()
                break
            self.show_board()
        print("Game finished.....")


if __name__ == "__main__":
    t = TicTacToeBoard()
    t.play()
