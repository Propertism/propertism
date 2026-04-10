web: python manage.py collectstatic --noinput --clear && gunicorn --bind 0.0.0.0:8000 --workers 2 --threads 15 realtor_project.wsgi:application
