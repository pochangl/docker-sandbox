import pytest
import re
from utils.tests.consumer import WebsocketCommunicator
from channels.testing import ChannelsLiveServerTestCase
from utils.asyncio import to_sync_func
from worker.tests.utils import setup_worker
from .utils import create_problem
from ..consumers import SubmissionConsumer


class WebsocketListenTest(ChannelsLiveServerTestCase):
    @to_sync_func
    @setup_worker
    async def test_submit(self):
        problem = create_problem(run_script='{% import_main %}\nmain.test()')
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
    async def test_notification(self):
        problem = create_problem(run_script='{% import_main %}\nmain.test()')
        pass_data = dict(
            value=dict(
                problem=problem.pk,
                code='def test(): print("stdout")',
            )
        )
        fail_data = dict(
            value=dict(
                problem=problem.pk,
                code='def test(): print("stdout"',
            )
        )
        async with WebsocketCommunicator(SubmissionConsumer, '/submission') as communicator:
            await communicator.send_json_to(pass_data)
            await communicator.receive_json_from(timeout=5)  # ignore result
            response = await communicator.receive_json_from(timeout=5)
            assert response == dict(type='notification', value='success')

            await communicator.send_json_to(fail_data)
            await communicator.receive_json_from(timeout=5)  # ignore result
            response = await communicator.receive_json_from(timeout=5)
            assert response == dict(type='notification', value='fail')

    @to_sync_func
    @setup_worker
    async def test_fail(self):
        problem = create_problem(run_script='{% import_main %}\nmain.test()')
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
            assert result['stdout'] == 'pass\n'

    @to_sync_func
    @setup_worker
    async def test_problem_image(self):
        'test if problem is run with specified image'

        async def run_problem(problem):
            'run problem and return result'
            async with WebsocketCommunicator(SubmissionConsumer, '/submission') as communicator:
                data = dict(
                    value=dict(
                        problem=problem.pk,
                        code='def test(): raise Exception(\'nope\')',
                    )
                )
                await communicator.send_json_to(data)
                response = await communicator.receive_json_from(timeout=5)
                return response['value']

        problem3_7 = create_problem(
            run_script='import sys\nprint(sys.version)',
            image='python:3.7',
        )

        problem3_8 = create_problem(
            run_script='import sys\nprint(sys.version)',
            image='python:3.8',
        )

        result = await run_problem(problem3_7)
        assert '3.7.' == result['stdout'][:4]

        result = await run_problem(problem3_8)
        assert '3.8.' == result['stdout'][:4]
