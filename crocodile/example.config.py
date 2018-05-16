from os import path


REDIS_URL = 'redis://localhost:6379/0'  # or other address for redis
CROCODILE_SECRET = 'secret_goes_here'
LOGFILE = 'crocodile.log'

CONSUMERSFILE = path.join(path.dirname(__file__), 'consumers.yml')
BROKER_TRANSPORT_OPTIONS = {
    'visibility_timeout': 3600
}
