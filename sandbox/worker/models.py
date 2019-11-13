import importlib
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from channels.layers import get_channel_layer


class Worker(models.Model):
    channel_name = models.CharField(max_length=1024, db_index=True)


class WorkerQueue(models.Model):
    channel_name = models.CharField(max_length=1024)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    model = GenericForeignKey('content_type', 'object_id')

    serializer_path = models.CharField(max_length=1024)

    @property
    def Serializer(self):
        module_name, serializer_name = self.serializer_path.rsplit('.', 1)
        module = importlib.import_module(module_name)
        return getattr(module, serializer_name)

    @property
    def serialized_data(self):
        return self.Serializer(instance=self.model).data

    async def receive(self, value):
        self.model.process_evaluation(value)

        layer = get_channel_layer()
        await layer.send(self.channel_name, dict(
            type='on_result',
            value=dict(
                type='result',
                value=self.serialized_data,
            )
        ))
