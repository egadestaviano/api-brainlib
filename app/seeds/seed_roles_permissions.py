import click
from flask import Flask
from app.seeds.roles_permissions import seed_roles_permissions
from app.db import database

def create_app() -> Flask:
    app = Flask(__name__)

    @app.cli.command("seed-roles")
    def seed_roles():
        """Seed roles and permissions"""
        if database.is_closed():
            database.connect()
        seed_roles_permissions()
        if not database.is_closed():
            database.close()

    return app
