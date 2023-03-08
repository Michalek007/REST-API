import os


class Config:
    """App configuration."""
    SCHEDULER_API_ENABLED = True
    LISTENER = {
        'host': '127.0.0.1',
        'port': 5000,
    }
    SERVER_NAME = f'{LISTENER["host"]}:{LISTENER["port"]}'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'database\\data.db')
    JWT_SECRET_KEY = "hkBxrbZ9Td4QEwgRewV6gZSVH4q78vBia4GBYuqd09SsiMsIjH"
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = False
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    TESTING = True
