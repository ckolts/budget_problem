from flask import Blueprint
from flask_apispec import marshal_with

from built_budgets_service import models
from built_budgets_service.budgets import schemas

BLUEPRINT = Blueprint('budgets', __name__)


@BLUEPRINT.route('/', methods=['GET'])
@marshal_with(schemas.BudgetSchema(many=True))
def list_budgets():
    return models.Budget.query.all()
