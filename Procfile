web: python biab/manage.py collectstatic --noinput; gunicorn --chdir biab biab.wsgi
worker: celery worker -A biab --workdir biab --loglevel=info
