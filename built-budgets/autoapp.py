"""Entrypoint into flask"""
from built_budgets_service.app import create_app


app = create_app()
