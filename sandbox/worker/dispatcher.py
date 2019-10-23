import asyncio
import collections
from . import executor

Result = collections.namedtuple('Result', ('stdout', 'stderr'), defaults=('', ''))

async def run(image: str, tag: str, text: str) -> str:
    await asyncio.sleep(1)

    try:
        return Result(stdout=executor.run(image, tag, text))
    except executor.ExecutionError as error:
        return Result(stderr=str(error))
