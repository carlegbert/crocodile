import subprocess
from celery import Celery
from crocodile import config


celery = Celery(
    'crocodile.hook.task',
    broker=config.REDIS_URL
)


@celery.task()
def build(consumer):
    subprocess.run(consumer.get('action'), shell=True)
