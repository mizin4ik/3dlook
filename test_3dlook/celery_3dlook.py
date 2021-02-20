from django.conf import settings

from celery import Celery
from celery.schedules import crontab
from kombu import Exchange, Queue

app = Celery('test_3dlook')

app.config_from_object('django.conf:settings', namespace='CELERY')


scheduled_tasks = {
    'notify_admin_about_new_users': {
        'task': 'notify_admin_about_new_users',
        'schedule': crontab(minute=1, hour=0)
    },
}

task_queues = (
    Queue(
        name='image_rotation',
        exchange=Exchange('image_rotation'),
        routing_key='image_rotation'
    ),
    Queue(
        name='mail',
        exchange=Exchange('mail'),
        routing_key='mail'
    ),
    Queue(
        name='default',
        exchange=Exchange('default'),
        routing_key='default'
    ),
)


task_routes = {
    'rotate_user_avatar': {'queue': 'image_rotation'},
    'notify_admin_about_new_users': {'queue': 'mail'}
}

app.conf.update(
    broker_url='redis://localhost:6379/9',
    result_backend='redis://localhost:6379/9',
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_queues=task_queues,
    task_default_queue='default',
    task_default_exchange='default',
    task_routes=task_routes,
    beat_schedule=scheduled_tasks,
    worker_max_tasks_per_child=512,
)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(settings.INSTALLED_APPS)
