import pytest
from channels.testing import WebsocketCommunicator
from .utils import create_problem
from ..consumers import SubmissionConsumer
from .. import models

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

    communicator = WebsocketCommunicator(SubmissionConsumer, '/submission')
    await communicator.connect()

    await communicator.send_json_to(data)
    response = await communicator.receive_json_from(timeout=5)
    assert response['type'] == 'result'
    result = response['value']

    assert result['stderr'] == ''
    assert result['stdout'] == 'stdout\n'
