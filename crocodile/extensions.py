from flask_redis import FlaskRedis

from crocodile.logging import register_logger


redis_store = FlaskRedis()


def init_extensions(app):
    redis_store.init_app(app)
    register_logger(app)
