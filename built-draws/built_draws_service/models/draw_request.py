"""Draw Request model"""
from sqlalchemy import Column, Integer, String

from built_draws_service.extensions import DB


class DrawRequest(DB.Model):
    """Draw Request model"""

    __tablename__ = 'draw_requests'

    # Model Schema
    draw_request_id = Column(Integer(), primary_key=True, nullable=False)
    budget_id = Column(Integer(), nullable=False)
    budget_item_id = Column(Integer(), nullable=False)
    amount = Column(String(20), nullable=False)
    effective_date = Column(String(40), nullable=False)
