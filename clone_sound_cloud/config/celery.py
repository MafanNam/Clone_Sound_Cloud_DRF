import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'send-spam-mail-every-week-at-8': {
        'task': 'oauth.tasks.send_spam_email_celery_task',
        'schedule': crontab(hour='17', minute='0', day_of_week='sat'),
    }
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
