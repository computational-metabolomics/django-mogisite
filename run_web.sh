#!/bin/sh


# prepare init migration
python manage.py makemigrations
# migrate db, so we have the latest db schema
python manage.py migrate

# add admin user
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin') if not User.objects.filter(username='admin') else None" | python manage.py shell

# start development server on public ip interface, on port 8000
python manage.py runserver 0.0.0.0:8000
