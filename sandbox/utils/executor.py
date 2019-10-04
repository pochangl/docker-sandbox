import tempfile
import contextlib
from . import docker


@contextlib.contextmanager
def TempFile(text):
    '''
        generate a temporary file with default content(text)
        return a read only file handler
    '''
    with tempfile.NamedTemporaryFile('w+', suffix='.py') as temp_file:
        temp_file.write(text)
        temp_file.flush()

        with open(temp_file.name, 'r') as reader:
            yield reader


def run(image: str, tag: str, text: str) -> str:
    ''' run python in docker '''
    with TempFile(text) as temp_file:
        return docker.run(
            image='{}:{}'.format(image, tag),
            command='python /main.py',
            volumes=docker.Volumes(
                [temp_file.name, '/main.py']
            )
        )
