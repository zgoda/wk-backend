import os


class Config:
    SECRET_KEY = os.getenv('WK_SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('WK_JWT_SECRET_KEY')
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_SAMESITE = 'Lax'
    JWT_TOKEN_LOCATION = ['cookies', 'headers']


class DevConfig(Config):
    JWT_COOKIE_SECURE = False


class TestConfig(Config):
    pass
