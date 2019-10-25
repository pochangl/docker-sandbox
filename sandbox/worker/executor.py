import collections
import json
import websockets
import tempfile
import contextlib
from functools import wraps
from . import docker


class ExecutionError(ValueError):
    def __init__(self, error):
        ''' convert error message to error class '''
        self.error = str(error.stderr, encoding='utf8')
        super().__init__(self.error)


@contextlib.contextmanager
def TransformError():
    ''' convert error to known error class '''
    try:
        yield
    except Exception as err:
        raise ExecutionError(err)


@contextlib.contextmanager
def TempFile(text=''):
    '''
        generate a temporary file with default content(text)
        return a read only file handler
    '''
    with tempfile.NamedTemporaryFile('w+', suffix='.py') as temp_file:
        temp_file.write(text)
        temp_file.flush()

        with open(temp_file.name, 'r') as reader:
            yield reader


def return_str(func):
    'convert binary to utf8 string'
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return str(result, encoding='utf8')
    return wrapper


@TransformError()
@return_str
def run(image: str, tag: str, text: str) -> str:
    ''' run python in docker '''
    with TempFile(text) as main:
        return docker.run(
            image='{}:{}'.format(image, tag),
            command='python /main.py',
            volumes=docker.Volumes(
                [main.name, '/main.py']
            )
        )


async def listen(host='ws://localhost:8000'):
    uri = '{}/ws/worker/'.format(host)
    async with websockets.connect(uri) as websocket:
        async for text in websocket:
            content = json.loads(text)
            result = dict(stdout='', stderr='', id=content.pop('id'))

            try:
                result['stdout'] = run(**content)
            except ExecutionError as error:
                result['stderr'] = str(error)
            await websocket.send(json.dumps(result))
