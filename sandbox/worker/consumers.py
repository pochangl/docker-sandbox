from channels.generic.websocket import AsyncJsonWebsocketConsumer
from . import models, dispatcher


class SandboxWorkerConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await super().connect()
        models.Worker.objects.create(channel_name=self.channel_name)

    async def receive_json(self, content):
        await dispatcher.receive_json(content)

    async def disconnect(self, code):
        models.Worker.objects.filter(channel_name=self.channel_name).delete()

    async def websocket_send(self, content):
        await self.send_json(content['value'])
