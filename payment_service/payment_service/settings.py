# settings.py
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

DATABASE_URL = config("DATABASE_URL", cast=Secret)
STRIPE_API_KEY = config("STRIPE_API_KEY", cast=Secret)
STRIPE_PUBLISHABLE_KEY = config("STRIPE_PUBLISHABLE_KEY", cast=Secret)
STRIPE_WEBHOOK_SECRET = config("STRIPE_WEBHOOK_SECRET", cast=Secret)