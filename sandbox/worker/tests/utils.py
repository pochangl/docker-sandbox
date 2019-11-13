import inspect
import asyncio
from utils.asyncio import run_background
from ..executor import listen


def setup_worker(func):
    assert inspect.iscoroutinefunction(func), '@setup_work only takes async func'
    async def wrapper(self, *args, **kwargs):
        async with run_background(listen(self.live_server_ws_url)):
            await asyncio.sleep(0.1)
            return await func(self=self, *args, **kwargs)
    return wrapper
