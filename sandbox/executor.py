import docker
import tempfile
import contextlib


@contextlib.contextmanager
def Client():
    ''' create a docker client and close it afterward'''
    client = docker.from_env()
    try:
        yield client
    except Exception as err:
        client.close()
        raise err
    client.close()


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


def run(image: str, tag: str, text: str) -> (str, str):
    ''' run python in docker '''
    with Client() as client, TempFile(text) as file:
        out = client.containers.run(
            image='{}:{}'.format(image, tag),
            command='python /main.py',
            volumes={
                file.name: dict(bind='/main.py', mode='ro')
            }
        )
    return out, ''
