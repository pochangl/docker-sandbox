import tempfile
import contextlib
from functools import wraps
from . import docker


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
