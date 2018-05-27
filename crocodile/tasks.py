import smtplib
import subprocess
from getpass import getuser
from socket import gethostname
from celery import Celery
from crocodile import config

_HOSTNAME = gethostname()
_USER = getuser()
_FROM = '%s@%s' % (_USER, _HOSTNAME)


celery = Celery(
    'crocodile.hook.task',
    broker=config.REDIS_URL
)


@celery.task()
def build(consumer):
    subprocess.run(consumer.get('action'), shell=True)


@celery.task()
def send_notification_email(mail):
    smtp = smtplib.SMTP('localhost')
    smtp.sendmail(_FROM, ','.join(mail.get('recipients')), mail.get('message'))
    smtp.close()
