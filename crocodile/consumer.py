from flask import current_app, request
import json
import yaml

from crocodile.extensions import redis_store
from crocodile.tasks import build


class Consumer(object):
    def __init__(self, event_type, ref, action):
        self.event_type = event_type
        self.ref = ref
        self.action = action

    def run(self):
        if current_app.config['TESTING']:
            return

        current_app.logger.info('Build initiated for %s:%s:%s'
                                % (self.event_type, self.ref, self.action))
        build.delay(self)

    @classmethod
    def load(cls, filename):
        with open(filename) as f:
            document = f.read()
        consumers = yaml.load(document, Loader=yaml.Loader)
        redis_store.delete('consumers')
        redis_store.set('consumers', json.dumps(consumers))

    @classmethod
    def get_all(cls):
        data = redis_store.get('consumers')
        return json.loads(data.decode('utf-8'))

    @classmethod
    def find_from_request(cls):
        data = request.get_json()
        ref = data.get('ref')
        event_type = request.headers.get('X-GitHub-Event')
        consumers = Consumer.get_all()
        event_consumers = consumers.get(event_type)
        action = event_consumers.get(ref)
        if not action:
            return None
        return Consumer(event_type, ref, action)
