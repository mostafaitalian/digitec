web: gunicorn config.wsgi:application
worker: celery worker --app=digitec.taskapp --loglevel=info
