import smtplib
import subprocess
from datetime import datetime
from getpass import getuser
from socket import gethostname
from celery import Celery
from crocodile import config

_HOSTNAME = gethostname()
_USER = getuser()
_FROM = '%s@%s' % (_USER, _HOSTNAME)


celery = Celery(
    'crocodile.hook.task',
    broker=config.REDIS_URL,
    backend=config.REDIS_URL,
)


@celery.task()
def build(consumer):
    start_time = datetime.now()
    repository = consumer.get('repository')
    watchers = consumer.get('watchers')
    event_type = consumer.get('event_type')
    ref = consumer.get('ref')
    action = consumer.get('action')

    started_msg = 'Build started at {} for application {} due to {} on {}.'\
        .format(start_time, repository, event_type, ref)
    send_notification_email.delay({'recipients': watchers,
                                   'message': started_msg})
    try:
        subprocess.run(action, check=True, shell=True, executable='/bin/bash')
        finished_msg = 'Build finished for %s' % repository
    except subprocess.CalledProcessError as e:
        finished_msg = 'Build failed for %s:\n%s' % (repository, str(e))
    end_time = datetime.now()
    mail = {'recipients': watchers,
            'message': '%s: %s' % (end_time, finished_msg)}
    send_notification_email.delay(mail)


@celery.task()
def send_notification_email(mail):
    smtp = smtplib.SMTP('localhost')
    smtp.sendmail(_FROM, ','.join(mail.get('recipients')), mail.get('message'))
    smtp.close()
