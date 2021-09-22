from flask import Blueprint
from flask_apispec import marshal_with

from built_draws_service import models
from built_draws_service.draw_requests import schemas

BLUEPRINT = Blueprint('draw-requests', __name__)


@BLUEPRINT.route('/', methods=['GET'])
@marshal_with(schemas.DrawRequestSchema(many=True))
def list_draw_requests():
    return models.DrawRequest.query.all()
