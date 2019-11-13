from channels import layers
from django.core.signing import Signer
from . import models


signer = Signer(salt='dispatcher')


async def send_json(channel_name, value):
    channel_layer = layers.get_channel_layer()
    value['id'] = signer.sign(value['id'])
    await channel_layer.send(channel_name, dict(
        type='websocket.send',
        value=value,
    ))


async def receive_json(value):
    pk = signer.unsign(value.pop('id'))
    queue = models.WorkerQueue.objects.get(pk=pk)
    await queue.receive(value)


async def run(queue, **kwargs) -> str:
    worker = models.Worker.objects.latest('id')  # bug: only the last work will get called

    await send_json(worker.channel_name, dict(id=queue.pk, **kwargs))
