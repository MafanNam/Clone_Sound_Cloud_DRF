import os

from celery import Celery
from celery.schedules import crontab

from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

# app.conf.beat_schedule = {
#     'send-mail-every-day-at-8': {
#         'task': 'oauth.tasks.send_spam_email',
#         'schedule': crontab(hour='17', minute='08'),
#         # 'args': (2,),
#     }
# }

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
