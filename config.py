import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod")
    # Read DB URL from environment. For local development the fallback remains SQLite.
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///bycodehub.db')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # If psycopg (psycopg3) is used, prefer SQLAlchemy driver scheme 'postgresql+psycopg'
    if DATABASE_URL and (DATABASE_URL.startswith('postgres://') or DATABASE_URL.startswith('postgresql://')):
        # If the URL doesn't already specify a driver, add '+psycopg' so SQLAlchemy uses psycopg3
        if 'postgresql+psycopg' not in DATABASE_URL and 'postgresql+psycopg://' not in DATABASE_URL:
            if DATABASE_URL.startswith('postgres://'):
                # normalize legacy postgres:// to postgresql+psycopg://
                SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace('postgres://', 'postgresql+psycopg://', 1)
            else:
                SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace('postgresql://', 'postgresql+psycopg://', 1)
        else:
            SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL

    # Engine options: when using PostgreSQL/Neon, ensure SSL is used.
    # Set PGSSLMODE env var to override (default: 'require').
    SQLALCHEMY_ENGINE_OPTIONS = {}
    if DATABASE_URL and (DATABASE_URL.startswith('postgres') or DATABASE_URL.startswith('postgresql')):
        sslmode = os.environ.get('PGSSLMODE', 'require')
        SQLALCHEMY_ENGINE_OPTIONS = {"connect_args": {"sslmode": sslmode}}

    # Mail Config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # Admin
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
