from channels.generic.websocket import AsyncJsonWebsocketConsumer
from . import models, serializers


class SubmissionConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive_json(self, content):
        serializer = serializers.SubmissionSerializer(data=content['value'])
        if serializer.is_valid():
            submission = serializer.save()
            await submission.evaluate()

            # return result
            result_serializer = serializers.SubmissionSerializer(instance=submission)
            await self.send_json(dict(
                type='result',
                value=result_serializer.data,
            ))
