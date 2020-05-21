"""Flask application entrypoint"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
from logging.config import dictConfig

from flask import Flask
from flask.logging import default_handler

import config
from blueprints import bp

from database.db import initialize_db


class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


def initialize_logger():
    """Set up logger format and level"""
    formatter = logging.Formatter(
        '[%(asctime)s]:[%(levelname)s]:[%(name)s]: %(message)s')

    default_handler.setFormatter(formatter)
    default_handler.setLevel(logging.DEBUG)

    wsgi_handler = logging.StreamHandler(
        stream='ext://flask.logging.wsgi_errors_stream')
    wsgi_handler.setFormatter(formatter)
    wsgi_handler.setLevel(logging.DEBUG)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(default_handler)

    # 3rd party loggers
    logging.getLogger('botocore').setLevel(logging.INFO)
    logging.getLogger('urllib3').setLevel(logging.INFO)


def create_app():
    """Factory to create the Flask application"""
    app = Flask(__name__)

    app.config.from_object('config')

    app.wsgi_app = ReverseProxied(app.wsgi_app)

    app.jinja_env.auto_reload = True

    initialize_db(app)

    app.register_blueprint(bp)

    return app


application = create_app()  # pylint: disable=C0103

if __name__ == '__main__':
    initialize_logger()
    application.run('0.0.0.0', port=config.PORT, debug=config.DEBUG)
