# implement minimax algorithm for tic tac toe
# Try alpha beta pruning as well

"""
Minimax(s: state):
    if Terminal(s):
        return Value(s)
    if Player(s) == MAX:
        value = -inf
        for a in Actions(s):
            value = Max(value, Minimax(Result(s, a)))
        return value
    if Player(s) == MIN:
        value = inf
        for a in Actions(s):
            value = Min(value, Minimax(Results(s, a)))
        return value
"""
import copy
import math
from typing import Any

from app_utils import constants


# TODO think about performance optimizations
def minimax_algorithm(
    board_object: Any,
    is_max_player: bool = True,
    row: int | None = None,
    col: int | None = None,
) -> int:
    # TODO Add proper documentation

    # Terminal state check
    # Board is full and no more moves left
    if board_object.is_board_full():
        return constants.MiniMaxConstants.DRAW, row, col

    # Game is complete with a player making a match
    elif row and col and board_object.is_game_complete(row=row, col=col):
        # Max lost if it is MAX turn to play but the game was complete in previous MIN turn. Reverse in MIN's turn to play
        return (
            (
                constants.MiniMaxConstants.MAX_LOSE
                if is_max_player
                else constants.MiniMaxConstants.MAX_WIN
            ),
            row,
            col,
        )

    # check if current player is max player
    if is_max_player:
        value = -math.inf
        # for some combinations
        # need to loop through free spaces and get it right
        for position in board_object.free_spaces:
            row = position // constants.BOARD_SIZE
            col = position % constants.BOARD_SIZE
            board_object.board[row][col] = (
                constants.TicTacToeArgs.X
                if board_object.start_role == constants.Role.BOT
                else constants.TicTacToeArgs.O
            )
            board_object.free_spaces.remove(position)
            calculated_value, _, _ = minimax_algorithm(
                board_object=copy(board_object),
                is_max_player=False,
                row=row,
                col=col,
            )
            max_value = max(value, calculated_value)
        return max_value, row, col

    else:
        value = math.inf
        # for loop to go thru possible actions
        for position in board_object.free_spaces:
            row = position // constants.BOARD_SIZE
            col = position % constants.BOARD_SIZE
            board_object.board[row][col] = (
                constants.TicTacToeArgs.X
                if board_object.start_role == constants.Role.BOT
                else constants.TicTacToeArgs.O
            )
            board_object.free_spaces.remove(position)
            calculated_value, _, _ = minimax_algorithm(
                board=copy(board_object), is_max_player=True, row=row, col=col
            )
            min_value = min(value, calculated_value)
        return min_value, row, col
