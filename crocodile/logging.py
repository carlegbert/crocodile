from flask import current_app, request
from functools import wraps
import logging
from logging.handlers import TimedRotatingFileHandler


class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url
        record.method = request.method
        record.remote_addr = request.environ.get('HTTP_X_REAL_IP',
                                                 request.remote_addr)
        return super().format(record)


def register_logger(app):
    logfile = app.config.get('LOGFILE', 'crocodile.log')
    handler = TimedRotatingFileHandler(logfile, when='d', interval=1)
    handler.setLevel(logging.INFO)
    formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s | %(method)s to %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)


def log_request(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_app.logger.info('request made')
        return fn(*args, **kwargs)

    return wrapper
