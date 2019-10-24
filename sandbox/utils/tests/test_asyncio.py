import asyncio
import pytest
from ..asyncio import run_background


@pytest.mark.asyncio
async def test_run_background():
    queue = []
    async def counter(number):
        while True:
            queue.append(number)
            await asyncio.sleep(0.01)

    async with run_background(counter(1)), run_background(counter(2)):
        queue.append(3)
        await asyncio.sleep(0.02)
        queue.append(3)
    assert queue == [1, 2, 3, 1, 2, 3]
