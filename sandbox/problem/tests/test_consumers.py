import contextlib
import pytest
from channels.testing import WebsocketCommunicator as BaseWebsocketCommunicator
from .utils import create_problem
from ..consumers import SubmissionConsumer
from .. import models


@contextlib.asynccontextmanager
async def WebsocketCommunicator(*args, **kwargs):
    communicator = BaseWebsocketCommunicator(*args, **kwargs)
    await communicator.connect()
    try:
        yield communicator
    finally:
        await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_submit():
    problem = create_problem(run_script='test()')
    data = dict(
        value=dict(
            problem=problem.pk,
            code='def test(): print("stdout")',
        )
    )
    async with WebsocketCommunicator(SubmissionConsumer, '/submission') as communicator:
        await communicator.connect()

        await communicator.send_json_to(data)
        response = await communicator.receive_json_from(timeout=5)
        assert response['type'] == 'result'
        result = response['value']

        assert result['stderr'] == ''
        assert result['stdout'] == 'stdout\n'
