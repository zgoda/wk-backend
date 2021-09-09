import os


class Config:
    SECRET_KEY = os.getenv('WK_SECRET_KEY')
    AUTH0_ALGORITHMS = ['RS256']
    AUTH0_JWKS_URI = f"https://{os.environ['AUTH0_DOMAIN']}/.well-known/jwks.json"
    AUTH0_ISSUER = f"https://{os.environ['AUTH0_DOMAIN']}/"
    AUTH0_AUDIENCE = os.environ['AUTH0_AUDIENCE']


class TestConfig(Config):
    pass
