#!/bin/sh

# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
su -m myuser -c "celery worker -A mogi_site.celery -Q default -n default@%h"