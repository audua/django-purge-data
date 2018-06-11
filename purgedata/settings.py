import os

SECRET_KEY = 'a@fq(d*4qdjl8a&@5f*!z$8fw$b&d%f+8f(vg9w0^i@z2w(m%c'

INSTALLED_APPS = [
    'purgedata',
    'django_celery_results',
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}