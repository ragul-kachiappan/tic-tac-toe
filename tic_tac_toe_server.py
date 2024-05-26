import json

import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from tic_tac_toe_game import board
from tic_tac_toe_game.app_utils import constants

templates = Jinja2Templates(directory="templates")

# t = board.TicTacToeBoard()
state = [
    [
        constants.TicTacToeArgs.X,
        constants.TicTacToeArgs.EMPTY,
        constants.TicTacToeArgs.X,
    ],
    [
        constants.TicTacToeArgs.EMPTY,
        constants.TicTacToeArgs.O,
        constants.TicTacToeArgs.EMPTY,
    ],
    [
        constants.TicTacToeArgs.O,
        constants.TicTacToeArgs.EMPTY,
        constants.TicTacToeArgs.O,
    ],
]


async def tic_tac_toe_page(request):
    # TODO get type of ai action from query params
    if request.method == "GET":
        current_board_state_str = request.cookies.get(
            "current_board_state", None
        )
        current_free_spaces_str = request.cookies.get(
            "current_free_spaces", None
        )
        current_board_state = (
            json.loads(current_board_state_str)
            if current_board_state_str
            else None
        )
        current_free_spaces = (
            json.loads(current_free_spaces_str)
            if current_free_spaces_str
            else None
        )
        game_board = board.TicTacToeBoard(
            current_board_state=current_board_state,
            current_free_spaces=current_free_spaces,
        )
        context = {"board": game_board.board}
        response = templates.TemplateResponse(
            request, "board_page.html", context=context
        )
        response.set_cookie(
            key="current_board_state", value=json.dumps(game_board.board)
        )
        response.set_cookie(
            key="current_free_spaces", value=json.dumps(game_board.free_spaces)
        )
        return response

    if request.method == "POST":
        pass


routes = [
    Route("/", endpoint=tic_tac_toe_page),
    Mount("/static", StaticFiles(directory="static"), name="static"),
]

app = Starlette(debug=True, routes=routes)

if __name__ == "__main__":
    config = uvicorn.Config(
        "tic_tac_toe_server:app", port=8000, log_level="info"
    )
    server = uvicorn.Server(config)
    server.run()
