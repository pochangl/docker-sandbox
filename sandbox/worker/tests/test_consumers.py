import asyncio
import pytest
from channels.testing import ChannelsLiveServerTestCase
from utils.tests.consumer import WebsocketCommunicator
from utils.asyncio import to_sync_func
from .utils import setup_worker
from ..consumers import SandboxWorkerConsumer
from .. import models


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_worker_registration():
    assert models.Worker.objects.count() == 0
    async with WebsocketCommunicator(SandboxWorkerConsumer, '/ws/worker/') as communicator:
        assert models.Worker.objects.count() == 1
    assert models.Worker.objects.count() == 0
