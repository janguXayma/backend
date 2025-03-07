from __future__ import absolute_import, unicode_literals
import os 
from celery import Celery

# set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# create the Celery application
app = Celery('backend')

# configure Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# load task modules from all registered apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))