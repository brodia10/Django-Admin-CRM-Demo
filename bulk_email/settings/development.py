from .base import *

DEBUG = True

UNSUBSCRIBE_ROUTE_BASE = "http://127.0.0.1:8000/email/unsubscribe"

ALLOWED_HOSTS += ["*"]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
