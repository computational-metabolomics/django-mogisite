import os
from .docker_check import is_docker

docker_flag = is_docker()

# Celery configuration
# Sensible settings for celery
CELERY_RESULT_BACKEND = 'django-db'
CELERY_WORKER_STATE_DB = 'django-db'
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_TASK_RESULT_EXPIRES = 6000
# Don't use pickle as serializer, json is much safer
# CELERY_TASK_SERIALIZER = "pickle"
CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ['pickle', 'application/json']
CELERYD_HIJACK_ROOT_LOGGER = False
CELERYD_PREFETCH_MULTIPLIER = 1
CELERYD_MAX_TASKS_PER_CHILD = 1000

if docker_flag:
    RABBIT_HOSTNAME = os.environ.get('RABBIT_PORT_5672_TCP', 'django-rabbitmq')
else:
    RABBIT_HOSTNAME = "0.0.0.0"

if RABBIT_HOSTNAME.startswith('tcp://'):
    RABBIT_HOSTNAME = RABBIT_HOSTNAME.split('//')[1]

BROKER_URL = os.environ.get('BROKER_URL',
                            '')
if not BROKER_URL:
    BROKER_URL = 'amqp://{user}:{password}@{hostname}/{vhost}/'.format(
        user=os.environ.get('RABBIT_ENV_USER', 'admin'),
        password=os.environ.get('RABBIT_ENV_RABBITMQ_PASS', 'mypass'),
        hostname=RABBIT_HOSTNAME,
        vhost=os.environ.get('RABBIT_ENV_VHOST', ''))

# We don't want to have dead connections stored on rabbitmq, so we have to negotiate using heartbeats
BROKER_HEARTBEAT = '?heartbeat=60'
if not BROKER_URL.endswith(BROKER_HEARTBEAT):
    BROKER_URL += BROKER_HEARTBEAT

BROKER_POOL_LIMIT = 1
BROKER_CONNECTION_TIMEOUT = 10
