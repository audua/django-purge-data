# Celery settings can be found here:
# http://docs.celeryproject.org/en/latest/userguide/configuration.html
import os
from celery.schedules import crontab

rabbit_user = os.getenv('RABBITMQ_USER', 'guest')
rabbit_pass = os.getenv('RABBITMQ_PASSWORD', 'guest')
rabbit_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbit_port = os.getenv('RABBITMQ_PORT', '5672')
rabbit_vhost = os.getenv('RABBITMQ_VHOSTNAME', '/')
broker_url = f'amqp://{rabbit_user}:{rabbit_pass}@{rabbit_host}:{rabbit_port}/{rabbit_vhost}'

result_backend = 'django-db'
accept_content = ['json']
task_serializer = 'json'

# Directions for scheduling periodic tasks:
# http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html
def get_crontab(env_var_name):
    env_val = os.getenv(env_var_name)
    if not env_val or env_val.upper() == 'DISABLED':
        return env_var_name

    tokens = env_val.split(' ')
    if len(tokens) == 1:
        return crontab(minute=tokens[0])
    if len(tokens) == 2:
        return crontab(minute=tokens[0], hour=tokens[1])
    if len(tokens) == 3:
        return crontab(minute=tokens[0], hour=tokens[1], day_of_week=tokens[2])
    return None


beat_schedule = {}


def add_schedule(name, task, env_var, args=None):
    ct = get_crontab(env_var)
    if not ct:
        return
    if not isinstance(ct, crontab):
        if not ct.replace('.', '', 1).isdigit():
            return
        ct = float(ct)
    beat_schedule[name] = {
        'task': task,
        'schedule': ct,
        'args': args
    }


#  add_schedule('purge-mymodel-data', 'purgedata.tasks.purge_data', 'PURGE_MYMODEL_DATA_SCHEDULE', ('purgedata.mymodel', '--filter=created_date__lte=180'))
#  add_schedule('purge-sample-data', 'purgedata.tasks.purge_data', '3600.0', ('purgedata.sample', '--filter=modified_date__lte=1'))

