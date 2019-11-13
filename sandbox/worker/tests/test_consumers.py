import pytest
from utils.tests.consumer import WebsocketCommunicator
from ..consumers import SandboxWorkerConsumer
from .. import models


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_worker_registration():
    assert models.Worker.objects.count() == 0
    async with WebsocketCommunicator(SandboxWorkerConsumer, '/ws/worker/'):
        assert models.Worker.objects.count() == 1
    assert models.Worker.objects.count() == 0
