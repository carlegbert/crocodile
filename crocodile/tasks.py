import smtplib
import subprocess
from socket import gethostname
from celery import Celery
from crocodile import config

_HOSTNAME = gethostname()
_FROM = 'crocodile %s' % _HOSTNAME


celery = Celery(
    'crocodile.hook.task',
    broker=config.REDIS_URL
)


@celery.task()
def build(consumer):
    subprocess.run(consumer.get('action'), shell=True)


@celery.task()
def send_notification_email(recipients, subject, message):
    smtp = smtplib.SMTP('localhost')
    smtp.sendmail(_FROM, recipients, message)
    smtp.close()
