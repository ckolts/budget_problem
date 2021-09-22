from marshmallow import Schema, fields


class DrawRequestSchema(Schema):
    draw_request_id = fields.Integer()
    budget_id = fields.Integer()
    budget_item_id = fields.Integer()
    amount = fields.String()
    effective_date = fields.String()
