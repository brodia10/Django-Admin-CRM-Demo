release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn bulk_email.wsgi