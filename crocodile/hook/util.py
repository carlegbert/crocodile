import json
import yaml

from crocodile.extensions import redis_store


def load_hooks(hooksfile):
    with open(hooksfile) as f:
        document = f.read()
    hooks = yaml.load(document, Loader=yaml.Loader)
    redis_store.delete('hooks')
    redis_store.set('hooks', json.dumps(hooks))


def get_hooks():
    hook_data = redis_store.get('hooks')
    return json.loads(hook_data.decode('utf-8'))
