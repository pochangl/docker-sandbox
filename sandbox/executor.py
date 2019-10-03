import tempfile
import contextlib
from . import docker


@contextlib.contextmanager
def TempFile(text):
    '''
        generate a temporary file with default content(text)
        return a read only file handler
    '''
    with tempfile.NamedTemporaryFile('w+', suffix='.py') as file:
        file.write(text)
        file.flush()

        with open(file.name, 'r') as f:
            yield f


@docker.TransformError()
def run(image: str, tag: str, text: str) -> str:
    ''' run python in docker '''
    with docker.Client() as client, TempFile(text) as temp_file:
        return client.containers.run(
            image='{}:{}'.format(image, tag),
            command='python /main.py',
            volumes={
                temp_file.name: dict(bind='/main.py', mode='ro')
            }
        )
