from aiohttp import web
from web.hooks import Hooks


def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


def build_webapp():
    hooks = Hooks()
    app = web.Application()
    app.add_routes([web.get('/', handle),
                    web.post('/hooks/{func}', hooks.call_func)])

    return app
