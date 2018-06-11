from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery import shared_task
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'purgedata.settings')
app = Celery('purgedata')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('purgedata.celeryconfig')


@shared_task(name='purgedata.tasks.purge_data')
def purge_data(app_and_model, *args):
    """This task runs on a schedule to purge data in the specified criteria.
    """
    call_command('purge_data', app_and_model, *args)
