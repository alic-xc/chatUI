release: python manage.py migrate

web: gunicorn chatUI.wsgi --log-file -

python manage.py collectstatic --noinput
python manage.py runserver
