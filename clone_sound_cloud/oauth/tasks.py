from time import sleep

from celery import shared_task

from django.contrib.auth import get_user_model

from config.celery import app
from oauth.email import ActivationEmail


@shared_task(bind=True)
def test_funk(self):
    for i in range(10):
        print(i)
        sleep(2)
    return 'Done'


@app.task(bind=True, default_retry_delay=5 * 60)
def send_activate_email(self, context, email):
    try:
        context['user'] = get_user_model().objects.get(id=context.get('user_id'))
        ActivationEmail(context=context).send(email)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
