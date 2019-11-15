import asyncio
import logging
import time
import websockets
from django.core.management.base import BaseCommand
from worker import executor


logger = logging.getLogger('django.sandbox.computeunit')


class Command(BaseCommand):
    def handle(self, *args, **options):
        while True:
            logger.info('connecting...')
            try:
                asyncio.run(executor.listen())
            except ConnectionRefusedError:
                logger.error('Cannot connect to server.')
            except websockets.exceptions.WebSocketException:
                logger.error('Websocket error.')

            time.sleep(10)
