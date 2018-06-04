from flask import current_app, request
import yaml

from crocodile.tasks import build


class Consumer(object):

    _consumers = {}

    def __init__(self, repository, event_type, ref, action, watchers):
        self.repository = repository
        self.event_type = event_type
        self.ref = ref
        self.action = action
        self.watchers = watchers

    def run(self):
        current_app.logger.info('Build initiated for %s:%s:%s:%s'
                                % (self.repository, self.event_type, self.ref,
                                   self.action))
        build.delay(**self.to_dict())

    def to_dict(self):
        return {
            'repository': self.repository,
            'event_type': self.event_type,
            'ref': self.ref,
            'action': self.action,
            'watchers': self.watchers
        }

    @classmethod
    def initialize_consumers(cls, filename):
        with open(filename) as f:
            document = f.read()
        consumers_raw = yaml.load(document, Loader=yaml.Loader)
        for repo in consumers_raw:
            cls._consumers[repo] = [Consumer(repository=repo, **c)
                                    for c in consumers_raw[repo]]

    @classmethod
    def find_from_request(cls):
        data = request.get_json()
        ref = data.get('ref')
        event_type = request.headers.get('X-GitHub-Event')
        repository = data.get('repository').get('full_name')
        repo_consumers = cls._consumers.get(repository)
        if not repo_consumers:
            return None
        for c in repo_consumers:
            if c.event_type == event_type and c.ref == ref:
                return c
        return None
