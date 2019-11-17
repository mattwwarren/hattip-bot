import asyncio

class Hooks:
    def call_func(self, request):
        func = request.match_info.get('func')
        if func and getattr(self, func):
            asyncio.ensure_future(func(body))

    async def echo(self, body):
        body = await request.json()
        print(body)
