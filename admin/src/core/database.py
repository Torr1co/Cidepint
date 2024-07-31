""" Database creation and management module"""
from enum import Enum

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

db = SQLAlchemy()


class HelperModel:
    """
    Custom helper functions for our DB models.
    """

    def serialize(self, exclude=[]):
        dicc = {}
        for c in inspect(self).mapper.column_attrs:
            if c.key not in exclude:
                dicc[c.key] = getattr(self, c.key)
        return dicc


def init_app(app):
    """
    DB app inicialization
    """
    db.init_app(app)
    config_db(app)


def config_db(app):
    """
    Configures the database app
    """

    @app.teardown_request
    def close_session(exception=None):
        db.session.close()


def reset_db():
    """
    Drops all tables and creates new ones
    """
    print("🧹 Dropping all tables...")
    db.drop_all()
    print("⚙️ Creating new tables...")
    db.create_all()
    db.session.commit()
    print("✅ Database reset done!")
