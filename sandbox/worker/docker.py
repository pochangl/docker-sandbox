import contextlib
import docker


def Client():
    ''' create a docker client and close it afterward'''
    return contextlib.closing(docker.from_env())


def Volumes(*pair):
    items = ((path, dict(bind=target, mode='ro')) for path, target in pair)
    return dict(items)


def run(**kwargs):
    with Client() as client:
        return client.containers.run(**kwargs)
