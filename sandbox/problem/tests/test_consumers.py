import pytest
import re
from utils.tests.consumer import WebsocketCommunicator
from channels.testing import ChannelsLiveServerTestCase
from utils.asyncio import to_sync_func
from worker.tests.utils import setup_worker
from .utils import create_problem
from ..consumers import SubmissionConsumer
from .. import models


class WebsocketListenTest(ChannelsLiveServerTestCase):
    @to_sync_func
    @setup_worker
    async def test_submit(self):
        problem = create_problem(run_script='test()')
        data = dict(
            value=dict(
                problem=problem.pk,
                code='def test(): print("stdout")',
            )
        )
        async with WebsocketCommunicator(SubmissionConsumer, '/submission') as communicator:
            await communicator.send_json_to(data)
            response = await communicator.receive_json_from(timeout=5)
            assert response['type'] == 'result'
            result = response['value']

            assert result['stderr'] == ''
            assert result['stdout'] == 'stdout\n'

    @to_sync_func
    @setup_worker
    async def test_fail(self):
        problem = create_problem(run_script='test()')
        data = dict(
            value=dict(
                problem=problem.pk,
                code='def test(): raise Exception(\'nope\')',
            )
        )
        async with WebsocketCommunicator(SubmissionConsumer, '/submission') as communicator:
            await communicator.send_json_to(data)
            response = await communicator.receive_json_from(timeout=5)
            assert response['type'] == 'result'
            result = response['value']

            assert re.search(r'Exception: nope\n$', result['stderr']), result['stderr']
            assert result['stdout'] == ''
