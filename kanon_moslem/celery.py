import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kanon_moslem.settings')

app = Celery('kanon_moslem')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
