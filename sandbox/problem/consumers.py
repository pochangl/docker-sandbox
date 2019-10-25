from channels.generic.websocket import AsyncJsonWebsocketConsumer
from worker.models import WorkerQueue
from worker import dispatcher
from . import models, serializers


class SubmissionConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive_json(self, content):
        serializer = serializers.SubmissionSerializer(data=content['value'])
        if serializer.is_valid():
            submission = serializer.save()
            queue = WorkerQueue.objects.create(
                channel_name=self.channel_name,
                model=submission,
                serializer_path='problem.serializers.SubmissionSerializer',
            )
            await dispatcher.run(queue=queue, **submission.run_params)

    async def websocket_send(self, content):
        await self.send_json(content['value'])
