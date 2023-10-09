# celery.py

import os
from celery import Celery
from django.conf import settings
from celery import Celery
from celery.schedules import crontab

app = Celery('commerce')


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'commerce.settings')

app = Celery('commerce')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    'check-auction-completion': {
        'task': 'myapp.tasks.check_auction_completion',
        'schedule': crontab(minute=52, hour=5),  # Runs daily at midnight
    },
}

