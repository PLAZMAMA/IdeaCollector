from celery import shared_task
from idea.models import IdeaModel
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from time import sleep

channel_layer = get_channel_layer()

@shared_task
def get_most_recent_ideas(num_of_ideas, most_recent_ideas):
    """gets the most recent "num_of_ideas" ideas"""
    last_most_recent_ideas = most_recent_ideas
    while(last_most_recent_ideas != most_recent_ideas):
        most_recent_ideas = IdeaModel.objects.all().order_by('-date_time')[:num_of_ideas]
        sleep(3)

    try:
        async_to_sync(channel_layer.group_send)('most_recent', {'type': 'get_most_recent','text': most_recent_ideas})
    except Exception as e:
        print(f'no on is connected to the websocket connection: {e}')