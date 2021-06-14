from .base import *
from decouple import config

DEBUG = False

UNSUBSCRIBE_ROUTE_BASE = "https://oppdashboard.com/email/unsubscribe"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

ALLOWED_HOSTS += [
    "www.oppdashboard.com",
    "www.oppdashboard.com/",
    "www.fidelis-opp-production.herokuapp.com/",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASS"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}


# This ensures that Django will be able to detect a secure connection
# properly on Heroku.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Redirect HTTP to HTTPS
SECURE_SSL_REDIRECT = True

## AWS Settings ##
##################

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.us-east-2.amazonaws.com"
AWS_LOCATION = "static"

AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
