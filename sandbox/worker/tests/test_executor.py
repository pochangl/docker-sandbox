import asyncio
import re
import contextlib
import pytest
from channels.testing import ChannelsLiveServerTestCase
from ..models import Worker
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
    return run('python', '3.7', files={
        '/run.py': text
    })


def test_hello_world():
    stdout = run_python('print("hello world")')
    assert stdout == 'hello world\n'


def test_exception():
    with assertRaisesRegex(ExecutionError, r'Exception: err\n$'):
        run_python('raise Exception("err")')
