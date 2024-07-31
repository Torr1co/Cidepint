"""Main project config classes"""

import os


class Config:
    """Global config variables"""

    CSRF_ENABLED = True
    JWT_DURATION = 3600
    SECRET_KEY = os.environ.get("SECRET_KEY", "password123")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg2://admin:password123@localhost:5433/postgres",
    )
    MESSAGE_FLASHING_OPTIONS = {"duration": 5}
    TESTING = False
    SESSION_TYPE = "filesystem"
    GOOGLE_CLIENT_ID = os.environ.get(
        "GOOGLE_CLIENT_ID",
    )
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")


class ProductionConfig(Config):
    """Production config variables"""

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    # Flask-Mail Gmail SMTP server settings
    MAIL_PORT = 465
    MAIL_USERNAME = "grupo27.cidepint@gmail.com"
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "iuyi jvcq fzxn qsjx")
    MAIL_USE_TLS = False
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_USE_SSL = True
    # Server config
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")
    DB_HOST = os.environ.get("DB_HOST")
    DB_NAME = os.environ.get("DB_NAME")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


class DevelopmentConfig(Config):
    """Production config variables"""

    # Flask-Mail Gmail SMTP server settings
    MAIL_PORT = 465
    MAIL_USERNAME = "grupo27.cidepint@gmail.com"
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "iuyi jvcq fzxn qsjx")
    MAIL_USE_TLS = False
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_USE_SSL = True


class TestingConfig(Config):
    """Production config variables"""

    TESTING = True
    # Flask-Mail Mailtrap SMTP server settings
    MAIL_PORT = 2525
    MAIL_USERNAME = "763ee8a2a9558f"
    MAIL_PASSWORD = "********544a"
    MAIL_USE_TLS = True
    MAIL_SERVER = "sandbox.smtp.mailtrap.io"
    MAIL_USE_SSL = False


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
}
