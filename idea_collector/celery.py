import os
from celery import Celery

#set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'idea_collector.settings')

#build celery app and get the created tasks
app = Celery('idea_collector')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'get_random_idea': {
        'task': 'tasks.get_random_idea',
        'schedule': 5.0
    }
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')