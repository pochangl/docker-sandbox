import re
import contextlib
import pytest
from ..executor import run, ExecutionError


@contextlib.contextmanager
def assertRaisesRegex(exception, regex):
    try:
        yield
    except exception as ex:
        assert re.search(regex, ex.args[0])
    else:
        assert False, 'exception {} not found'.format(exception)


def run_python(text: str):
    return run('python', '3.7', text)


@pytest.mark.asyncio
async def test_hello_world():
    stdout = await run_python('print("hello world")')
    assert stdout == 'hello world\n'


@pytest.mark.asyncio
async def test_exception():
    with assertRaisesRegex(ExecutionError, r'Exception: err\n$'):
        await run_python('raise Exception("err")')
