import contextlib
from channels.testing import WebsocketCommunicator as BaseWebsocketCommunicator


@contextlib.asynccontextmanager
async def WebsocketCommunicator(*args, **kwargs):
    communicator = BaseWebsocketCommunicator(*args, **kwargs)
    await communicator.connect()
    try:
        yield communicator
    finally:
        await communicator.disconnect()
