"""Main flask app controller"""
import os

from dotenv import load_dotenv
from flask import Flask, abort, request, session

from flask_session import Session
from src.core import database
from src.core.crypto import cipher
from src.core.email import mail
from src.dbo import configuration_dbo
from src.web.config import config
from src.web.controllers import blueprints
from src.web.controllers.auth import logout
from src.web.utils import auth, cors, navigation, seed_helper
from src.web.utils import session as session_utils
from src.web.utils.compiler import TailwindCompiler
from src.web.utils.jwt import jwt_auth
from src.web.utils.oauth import oauth

load_dotenv()
session = Session()
tailwind = TailwindCompiler()


def create_app(env="development", static_folder="../../static"):
    """creating app with routing, configuration, db and tailwind"""
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])
    database.init_app(app)
    session.init_app(app)
    cipher.init_app(app)
    jwt_auth.init_app(app)
    mail.init_app(app)
    cors.init_app(app)
    tailwind.init_app(app)
    oauth.init_app(app)
    oauth.register(
        name="google",
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

    @app.before_request
    def check_maintenance_mode():
        if (
            auth.is_logged_in()
            and configuration_dbo.get_maintenance_mode()
            and session_utils.get_role() != "SUPERADMIN"
            and not request.path.startswith("/static")
        ):
            logout()
            abort(503)

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    @app.context_processor
    def inject_menu():
        menu = navigation.get_menu()
        return dict(menu=menu)

    @app.cli.command("resetdb")
    def resetdb():
        """Resets the database."""
        database.reset_db()

    @app.cli.command("seeddb")
    def seeddb():
        """Loads the db with mockup data."""
        seed_helper.seed_db()

    return app
