#!/bin/bash

# pyhton manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@dev.org', 'adminpass')"
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

