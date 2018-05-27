from datetime import datetime
from flask import current_app, request
import yaml

from crocodile.tasks import build, send_notification_email


class Consumer(object):

    _consumer_list = []

    def __init__(self, name, event_type, ref, action, watchers):
        self.name = name
        self.event_type = event_type
        self.ref = ref
        self.action = action
        self.watchers = watchers

    def run(self):
        if current_app.config['TESTING']:
            return

        current_app.logger.info('Build initiated for %s:%s:%s:%s'
                                % (self.name, self.event_type, self.ref,
                                   self.action))
        self._notify_build_started()
        build.delay(self.to_dict())
        build.delay(self)

    def to_dict(self):
        return {
            'event_type': self.event_type,
            'ref': self.ref,
            'action': self.action
        }

    def _notify_build_started(self):
        time = datetime.now()
        subject = 'Build started for %s' % self.name
        message = 'Build was triggered at %s for application %s due to %s'
        'event for branch %s' % (time, self.name, self.event_type,
                                 self.ref)
        send_notification_email(self.watchers, subject, message)

    @classmethod
    def from_dict(cls, d):
        pass

    @classmethod
    def initialize_consumers(cls, filename):
        with open(filename) as f:
            document = f.read()
        consumers_raw = yaml.load(document, Loader=yaml.Loader)
        cls._consumer_list = [Consumer(**c) for c in consumers_raw]

    @classmethod
    def find_from_request(cls):
        data = request.get_json()
        ref = data.get('ref')
        event_type = request.headers.get('X-GitHub-Event')
        for c in cls._consumer_list:
            if c.event_type == event_type and c.ref == ref:
                return c
        return None
