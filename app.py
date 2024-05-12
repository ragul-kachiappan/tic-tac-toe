# from starlette.responses import HTMLResponse
# from starlette.applications import Starlette
# from starlette.routing import Route
# import uvicorn

# async def game(scope, receive, send):
#     assert scope['type'] == 'http'
#     response = HTMLResponse(content='<html><body><h1>Hello, world!</h1></body></html>')
#     await response(scope, receive, send)

# app = Starlette(debug=True, routes=[
#     Route('/', game),
# ])


# if __name__ == "__main__":
#     uvicorn.run("app:app", port=8000, log_level="info")

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


async def homepage(request):
    return JSONResponse({'hello': 'world'})


app = Starlette(debug=True, routes=[
    Route('/', homepage),
])