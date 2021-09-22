from marshmallow import Schema, fields


class BudgetItemSchema(Schema):
    budget_item_id = fields.Integer()
    budget_id = fields.Integer()
    original_amount = fields.String()
    funded_to_date = fields.String()
