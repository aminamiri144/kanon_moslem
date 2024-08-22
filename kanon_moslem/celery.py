import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kanon_moslem.settings')

app = Celery('kanon_moslem')

app.config_from_object('django.conf:settings', namespace='CELERY')

# app.conf.beat_schedule = {
#     'generate_weekly_time_slots': {
#         'task': 'reserveTime.tasks.create_week_time_slots',
#         'schedule': crontab(minute='0', hour='0'),
#     },
#     'disable_expired_timeslots': {
#         'task': 'reserveTime.tasks.disable_expired_timeslots',
#         'schedule': crontab(minute='2', hour='0'),
#     },
#     'test_celery_beat_on_server': {
#         'task': 'reserveTime.tasks.test_celery_beat_on_server',
#         'schedule': crontab(minute='0', hour='*/2'),
#     },
# }

app.autodiscover_tasks()
