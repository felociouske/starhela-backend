release: python manage.py migrate && python manage.py seed_payment_methods
web: gunicorn config.wsgi --bind 0.0.0.0:$PORT
