from time import sleep

from django.conf import settings

from django.contrib.auth import get_user_model
from django.core.mail import send_mass_mail

from config.celery import app

from oauth import email as email_modul

User = get_user_model()


@app.task(bind=True, default_retry_delay=5 * 60)
def send_email_celery_task(self, context, email, sender):
    try:
        context['user'] = User.objects.get(id=context.get('user_id'))
        match sender:
            case 'ActivationEmail':
                email_modul.ActivationEmail(context=context).send(email)
            case 'ConfirmationEmail':
                email_modul.ConfirmationEmail(context=context).send(email)
            case 'PasswordChangedConfirmationEmail':
                email_modul.PasswordChangedConfirmationEmail(context=context).send(email)
            case 'PasswordResetEmail':
                email_modul.PasswordResetEmail(context=context).send(email)
            case 'UsernameChangedConfirmationEmail':
                email_modul.UsernameChangedConfirmationEmail(context=context).send(email)
            case 'UsernameResetEmail':
                email_modul.UsernameResetEmail(context=context).send(email)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
    return 'Done'


@app.task(bind=True, default_retry_delay=5 * 60)
def send_spam_email_celery_task(self):
    try:
        users = User.objects.filter(is_spam_email=True, is_active=True)
        subject = 'Test spam mass email with celery'
        message = 'Testing'
        from_email = settings.EMAIL_HOST_USER
        messages = [(subject, message, from_email, [user.email]) for user in users]
        send_mass_mail(messages, fail_silently=True)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
    return 'Done'
