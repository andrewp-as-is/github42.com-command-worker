import asyncio
from datetime import datetime, timedelta
import logging
import os
import sys
from traceback import format_exception

from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.management.base import BaseCommand

from base.apps.http.models import Request
from .utils import push_tasks, run_task

RESTART_SECONDS = float(getattr(settings,'ASYNCIO_TASK_QUEUE_RESTART_SECONDS',None) or 0)
SLEEP_SECONDS = float(getattr(settings,'ASYNCIO_TASK_QUEUE_SLEEP',0.1) or 0)


class Command(BaseCommand):
    q = None
    models = None
    sleep_seconds = None
    workers_count = None

    def add_arguments(self , parser):
        parser.add_argument('workers_count', type=int)

    def handle(self, *args, **options):
        Request.objects.filter(is_pushed=True).update(is_pushed=False)
        self.options = options
        self.q = asyncio.Queue()
        ioloop = asyncio.get_event_loop()
        ioloop.run_until_complete(asyncio.wait(self.get_aws(self.q)))
        ioloop.close()

    def get_aws(self,q):
        ioloop = asyncio.get_event_loop()
        aws = [
            ioloop.create_task(self.push_tasks_loop(q)),
            ioloop.create_task(self.restart_loop())
        ]
        for _ in range(1, self.get_workers_count() + 1):
            aws.append(ioloop.create_task(self.worker_loop(q)))
        return aws

    def get_sleep_seconds(self):
        return self.sleep_seconds if self.sleep_seconds else SLEEP_SECONDS

    def get_workers_count(self):
        return self.workers_count if self.workers_count else self.options.get('workers_count')

    async def restart_loop(self):
        while True:
            if STARTED_AT + timedelta(seconds=RESTART_SECONDS) < datetime.now():
                sys.exit(0)
            await asyncio.sleep(10)

    async def push_tasks_loop(self,q):
        try:
            count = 0
            sleep_seconds = self.get_sleep_seconds()
            while True:
                await asyncio.sleep(sleep_seconds)
                await push_tasks(q)
        except Exception as e:
            logging.error(e)
        finally:
            sys.exit(0)

    async def worker_loop(self,q):
        try:
            while True:
                try:
                    task = await q.get()
                    await run_task(task)
                    q.task_done()
                    await asyncio.sleep(0.01)
                except asyncio.QueueEmpty:
                    await asyncio.sleep(1)
        except Exception as e:
            logging.error(e)
            if settings.DEBUG:
                exc_traceback=''.join(format_exception(etype=type(e), value=e, tb=e.__traceback__))
                print(exc_traceback)
        finally:
            sys.exit(0)
