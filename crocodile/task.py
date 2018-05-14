import subprocess
from celery import Celery
from crocodile import config


celery = Celery(
    'crocodile.hook.task',
    broker=config.REDIS_URL
)


@celery.task()
def celery_build(hook_action):
    subprocess.run(hook_action, shell=True)
