import asyncio

class Hooks:
    def call_func(self, request):
        func = request.match_info.get('func')
        try:
            cls_func = getattr(self, func)
            asyncio.ensure_future(cls_func(request))
        except AttributeError as e:
            print('%s is not implemented.' % func)

    async def echo(self, request):
        body = await request.json()
        print(body)
