import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


async def tic_tac_toe_page(request):
    # TODO get type of ai action from query params
    return templates.TemplateResponse(request, "board_page.html")


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
