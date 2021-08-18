import asyncio
import time


async def main():
    print('main')
    task = asyncio.create_task(foo('foo'))
    print('after task foo()')


async def foo(text):
    print(text)
    await asyncio.sleep(5)


asyncio.run(main())
