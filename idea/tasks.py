from celery import shared_task
from idea.models import IdeaModel
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from time import sleep

channel_layer = get_channel_layer()

@shared_task
def publish_most_recent_ideas(self, num_of_ideas=5):
    """gets the most recent "num_of_ideas" ideas"""
    most_recent_ideas = IdeaModel.objects.all().order_by('-date_time')[:num_of_ideas]

    try:
        async_to_sync(channel_layer.group_send)('most_recent', {'type': 'get_most_recent','text': most_recent_ideas})
    except Exception as e:
        raise self.retry(f'no one is connected to the websocket connection but just in case, the function will run again(retry): {e}')