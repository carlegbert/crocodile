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
def build(*, repository, watchers, event_type, ref, action):
    try:
        subprocess.run(action, check=True, shell=True, executable='/bin/bash')
        msg = 'Build succeeded for %s' % repository
    except subprocess.CalledProcessError as e:
        msg = 'Build failed for %s:\n%s' % (repository, str(e))

    smtp = smtplib.SMTP('localhost')
    smtp.sendmail(_FROM, ','.join(watchers), msg)
    smtp.close()
