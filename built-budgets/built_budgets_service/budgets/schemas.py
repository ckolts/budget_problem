from marshmallow import Schema, fields


class BudgetSchema(Schema):
    budget_id = fields.Integer()
    amount = fields.String()
    balance_remaining = fields.String()
