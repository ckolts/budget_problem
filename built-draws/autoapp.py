"""Entrypoint into flask"""
from built_draws_service.app import create_app


app = create_app()
