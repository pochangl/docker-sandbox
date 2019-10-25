import asyncio
from django.core.management.base import BaseCommand
from worker import executor


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('listening')
        asyncio.run(executor.listen())
