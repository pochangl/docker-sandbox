from channels.generic.websocket import JsonWebsocketConsumer
from . import models, serializers


class SubmissionConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def receive_json(self, content):
        serializer = serializers.SubmissionSerializer(data=content['value'])
        if serializer.is_valid():
            submission = serializer.save()
            submission.evaluate()

            # return result
            result_serializer = serializers.SubmissionSerializer(instance=submission)
            self.send_json(dict(
                type='result',
                value=result_serializer.data,
            ))
