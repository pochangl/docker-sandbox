import contextlib
import docker
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
def TransformError():
    ''' convert error to known error class '''
    try:
        yield
    except errors.ContainerError as err:
        raise ExecutionError(err)


@TransformError()
def run(**kwargs):
    with Client() as client:
        return client.containers.run(**kwargs)
