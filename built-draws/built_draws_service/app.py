import os

from flask import Flask

from built_draws_service.draw_requests.views import BLUEPRINT as DRAW_REQUESTS_BLUEPRINT
from built_draws_service.extensions import DB
from built_draws_service.models.database_helpers import get_connection_string


class FlaskConfig:
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = get_connection_string()
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_app() -> Flask:
    """App creation factory

    :returns: An instance of a flask app
    :rtype: Flask.wsgi_app
    """

    app = Flask(__name__.split('.')[0])
    app.config.from_object(FlaskConfig)

    register_blueprints(app)
    register_extensions(app)

    return app


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(DRAW_REQUESTS_BLUEPRINT, url_prefix='/requests')


def register_extensions(app: Flask) -> None:
    DB.init_app(app)
