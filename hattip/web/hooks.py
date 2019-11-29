import asyncio
from aiohttp import web
from json.decoder import JSONDecodeError
from urllib.parse import parse_qsl


class Hooks:
    def call_func(self, request):
        func = request.match_info.get('func')
        try:
            cls_func = getattr(self, func)
            asyncio.ensure_future(cls_func(request))
        except AttributeError as e:
            print('%s is not implemented.' % func)

    async def echo(self, request):
        try:
            body = await request.json()
            print(body)
        except JSONDecodeError:
            body = await request.text()
            print(parse_qsl(body))
        except Exception as e:
            print(await request.text())
            raise e

        return web.Response(text="OK")
