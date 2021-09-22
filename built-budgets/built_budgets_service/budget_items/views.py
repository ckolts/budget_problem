from flask import Blueprint
from flask_apispec import marshal_with

from built_budgets_service import models
from built_budgets_service.budget_items import schemas

BLUEPRINT = Blueprint('items', __name__)


@BLUEPRINT.route('/', methods=['GET'])
@marshal_with(schemas.BudgetItemSchema(many=True))
def list_budget_items():
    return models.BudgetItem.query.all()
