import json
import yaml

from crocodile.extensions import redis_store


def load_consumers(consumersfile):
    with open(consumersfile) as f:
        document = f.read()
    consumers = yaml.load(document, Loader=yaml.Loader)
    redis_store.delete('consumers')
    redis_store.set('consumers', json.dumps(consumers))


def get_consumers():
    data = redis_store.get('consumers')
    return json.loads(data.decode('utf-8'))


def find_consumer(event_type, ref):
    consumers = get_consumers()
    event_consumers = consumers.get(event_type)
    if not event_consumers:
        return None
    return event_consumers.get(ref)
