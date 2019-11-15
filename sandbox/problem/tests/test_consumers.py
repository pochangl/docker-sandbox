import pytest
import re
from utils.tests.consumer import WebsocketCommunicator
from channels.testing import ChannelsLiveServerTestCase
from utils.asyncio import to_sync_func
from worker.tests.utils import setup_worker
from .utils import create_problem
from ..consumers import SubmissionConsumer


async def run_problem(problem, code: str='pass'):
    'run problem and return result and notification'
    async with WebsocketCommunicator(SubmissionConsumer, '/submission') as communicator:
        data = dict(
            value=dict(
                problem=problem.pk,
                code=code,
            )
        )
        await communicator.send_json_to(data)
        response = await communicator.receive_json_from(timeout=5)
        notification = await communicator.receive_json_from(timeout=5)
        return response, notification


class WebsocketListenTest(ChannelsLiveServerTestCase):
    @to_sync_func
    @setup_worker
    async def test_submit(self):
        problem = create_problem(run_script='{% import_main %}\nmain.test()')

        response, _ = await run_problem(problem=problem, code='def test(): print("stdout")')
        assert response['type'] == 'result'
        result = response['value']

        assert result['stderr'] == ''
        assert result['stdout'] == 'stdout\n'

    @to_sync_func
    @setup_worker
    async def test_notification(self):
        problem = create_problem(run_script='{% import_main %}\nmain.test()')

        _, notification = await run_problem(problem=problem, code='def test(): print("stdout")')
        assert notification == dict(type='notification', value='success')

        _, notification = await run_problem(problem=problem, code='def test(): print("stdout"')
        assert notification == dict(type='notification', value='fail')

    @to_sync_func
    @setup_worker
    async def test_fail(self):
        problem = create_problem(run_script='{% import_main %}\nmain.test()')

        response, _ = await run_problem(problem=problem, code='def test(): raise Exception(\'nope\')')
        assert response['type'] == 'result'
        result = response['value']

        assert re.search(r'Exception: nope\n$', result['stderr']), result['stderr']
        assert result['stdout'] == ''

    @to_sync_func
    @setup_worker
    async def test_with_statement(self):
        problem = create_problem(run_script='''
            import contextlib
            {% import_main %}
            with contextlib.suppress(Exception):
                main.test()
            print('pass')
        '''.replace('\n            ', '\n'))

        response, _ = await run_problem(problem=problem, code='def test(): raise Exception(\'nope\')')

        assert response['type'] == 'result'
        result = response['value']
        assert result['stdout'] == 'pass\n'

    @to_sync_func
    @setup_worker
    async def test_problem_image(self):
        'test if problem is run with specified image'

        problem3_7 = create_problem(
            run_script='import sys\nprint(sys.version)',
            image='python:3.7',
        )

        problem3_8 = create_problem(
            run_script='import sys\nprint(sys.version)',
            image='python:3.8',
        )

        response, _ = await run_problem(problem=problem3_7)
        assert '3.7.' == response['value']['stdout'][:4]

        response, _ = await run_problem(problem=problem3_8)
        assert '3.8.' == response['value']['stdout'][:4]
