import os

from flask import Flask

from built_budgets_service.budget_items.views import BLUEPRINT as BUDGET_ITEMS_BLUEPRINT
from built_budgets_service.budgets.views import BLUEPRINT as BUDGETS_BLUEPRINT
from built_budgets_service.extensions import DB
from built_budgets_service.models.database_helpers import get_connection_string


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
    app.register_blueprint(BUDGETS_BLUEPRINT, url_prefix='/budgets')
    app.register_blueprint(BUDGET_ITEMS_BLUEPRINT, url_prefix='/items')


def register_extensions(app: Flask) -> None:
    DB.init_app(app)
