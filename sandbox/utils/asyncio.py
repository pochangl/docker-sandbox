import asyncio
import contextlib


@contextlib.asynccontextmanager
async def run_background(coroutine):
    'run temporary background service within the context'

    assert asyncio.iscoroutine(coroutine), 'must be coroutine'
    task = asyncio.ensure_future(coroutine)
    await asyncio.sleep(0)
    yield
    task.cancel()
