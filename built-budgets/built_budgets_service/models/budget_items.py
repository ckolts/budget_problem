"""Budget Item model"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from built_budgets_service.extensions import DB


class BudgetItem(DB.Model):
    """Budget Item model"""

    __tablename__ = 'budget_items'

    # Model Schema
    budget_item_id = Column(Integer(), primary_key=True, nullable=False)
    budget_id = Column(
        Integer(), ForeignKey('budgets.budget_id'), nullable=False
    )
    funded_to_date = Column(String(20), nullable=False)
    original_amount = Column(String(20), nullable=False)

    # Model Relationships
    budget = relationship('Budget', uselist=False)
