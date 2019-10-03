import docker
import tempfile
import contextlib
from docker import errors


class ExecutionError(ValueError):
    def __init__(self, error):
        ''' convert error message to error class '''
        self.error = str(error.stderr, encoding='utf8')
        super().__init__(self.error)


def Client():
    ''' create a docker client and close it afterward'''
    return contextlib.closing(docker.from_env())


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


@contextlib.contextmanager
def TransformError():
    ''' convert error to known error class '''
    try:
        yield
    except errors.ContainerError as err:
        raise ExecutionError(err)


@TransformError()
def run(image: str, tag: str, text: str) -> str:
    ''' run python in docker '''
    with Client() as client, TempFile(text) as temp_file:
        return client.containers.run(
            image='{}:{}'.format(image, tag),
            command='python /main.py',
            volumes={
                temp_file.name: dict(bind='/main.py', mode='ro')
            }
        )
