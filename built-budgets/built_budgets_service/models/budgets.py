"""Budget model"""
from functools import reduce

from sqlalchemy import Column, Integer
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from built_budgets_service.extensions import DB


class Budget(DB.Model):
    """Budget model"""

    __tablename__ = 'budgets'

    # Model Schema
    budget_id = Column(Integer(), primary_key=True, nullable=False)

    # Model Relationships
    budget_items = relationship('BudgetItem', uselist=True)

    @hybrid_property
    def amount(self):
        return sum(int(item.original_amount) for item in self.budget_items)

    @hybrid_property
    def balance_remaining(self):
        funded_to_date: int = sum(int(item.funded_to_date) for item in self.budget_items)
        return self.amount - funded_to_date
