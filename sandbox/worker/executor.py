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
def run(image: str, files: '{ filename: code }') -> str:
    ''' run python in docker '''
    with contextlib.ExitStack() as stack:
        volumes = [
            (stack.enter_context(TempFile(code)).name, name)
            for name, code in files.items()]
        return docker.run(
            image=image,
            command='python /run.py',
            volumes=docker.Volumes(*volumes)
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
