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

from tic_tac_toe_game.app_utils import constants


def is_game_complete(
    state: list[list[int]],
    row: int,
    col: int,
) -> bool:
    check_row = map(lambda x: x == state[row][col], state[row])
    is_row_same = all(check_row)
    check_col = [
        state[i][col] == state[row][col] for i in range(constants.BOARD_SIZE)
    ]

    is_col_same = all(check_col)
    check_consecutive_marks = bool(is_row_same + is_col_same)

    if (row + col + 1) == constants.BOARD_SIZE:
        check_diag = [
            state[i][constants.BOARD_SIZE - 1 - i] == state[row][col]
            for i in range(constants.BOARD_SIZE)
        ]
        is_diag_same = all(check_diag)
        check_consecutive_marks = bool(check_consecutive_marks + is_diag_same)

    if row == col:
        check_diag = [
            state[i][i] == state[row][col] for i in range(constants.BOARD_SIZE)
        ]
        is_diag_same = all(check_diag)
        check_consecutive_marks = bool(check_consecutive_marks + is_diag_same)

    return check_consecutive_marks


# TODO think about performance optimizations
def minimax_algorithm(
    state: list[list[int]],
    free_spaces: list[int],
    start_role: constants.Role,
    is_max_player: bool = True,
    row: int | None = None,
    col: int | None = None,
) -> int:
    """
    Implementation of minimax algorithm.
        Params:
            state (list[list[int]]): represent the current state of tic tac toe board.
            free_spaces (list[int]): free spaces available in the board.
            start_role (Role): To determine whether user or bot had start role.
            is_max_player (bool): denotes whether max is making the first move.
            row (int | None): row index of the current action.
            col (int | None): col index of the current action.
        Returns:
            chosen_weight (int): chosen weight of terminal state based minimax criteria.
    """
    # terminal state check

    # check if the board is full
    if len(free_spaces) == 0:
        return constants.MiniMaxConstants.DRAW, row, col
    # check if the game is complete
    elif row and col and is_game_complete(state=state, row=row, col=col):
        return (
            (
                constants.MiniMaxConstants.MAX_LOSE
                if is_max_player
                else constants.MiniMaxConstants.MAX_WIN
            ),
            row,
            col,
        )

    # max player logic
    if is_max_player:
        value = -math.inf
        max_row = row
        max_col = col

        for position in free_spaces:
            row = position // constants.BOARD_SIZE
            col = position % constants.BOARD_SIZE
            state[row][col] = (
                constants.TicTacToeArgs.X
                if start_role == constants.Role.BOT
                else constants.TicTacToeArgs.O
            )
            recursive_call_state = copy.deepcopy(state)
            recursive_call_free_spaces = copy.deepcopy(free_spaces)
            recursive_call_free_spaces.remove(position)
            calculated_value, _, _ = minimax_algorithm(
                state=recursive_call_state,
                free_spaces=recursive_call_free_spaces,
                start_role=start_role,
                is_max_player=False,
                row=row,
                col=col,
            )
            if calculated_value > value:
                value = calculated_value
                max_row = row
                max_col = col

        return value, max_row, max_col

    # min player logic
    else:
        value = math.inf
        max_row = row
        max_col = col

        for position in free_spaces:
            row = position // constants.BOARD_SIZE
            col = position % constants.BOARD_SIZE
            state[row][col] = (
                constants.TicTacToeArgs.X
                if start_role == constants.Role.USER
                else constants.TicTacToeArgs.O
            )
            recursive_call_state = copy.deepcopy(state)
            recursive_call_free_spaces = copy.deepcopy(free_spaces)
            recursive_call_free_spaces.remove(position)
            calculated_value, _, _ = minimax_algorithm(
                state=recursive_call_state,
                free_spaces=recursive_call_free_spaces,
                start_role=start_role,
                is_max_player=True,
                row=row,
                col=col,
            )
            if calculated_value < value:
                value = calculated_value
                max_row = row
                max_col = col
        return value, max_row, max_col
