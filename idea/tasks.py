from celery import shared_task
from idea.models import IdeaModel
from idea.serializers import IdeaSerializer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from time import sleep
from random import randint

channel_layer = get_channel_layer()

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 5})
def publish_most_recent_ideas(self, num_of_ideas=5):
    """gets the most recent "num_of_ideas" ideas"""
    queryset = IdeaModel.objects.all().order_by('-date_time')[:num_of_ideas]
    most_recent_ideas = IdeaSerializer(queryset, many=True)
    try:
        async_to_sync(channel_layer.group_send)('most_recent', {'type': 'send_most_recent', 'text': most_recent_ideas})

    except Exception as e:
        raise Exception(f'no one is connected to the websocket connection but just in case, the function will run again(retry) in 5 seconds: {e}')

@shared_task
def get_random_idea():
    """get a random idea"""
    queryset = IdeaModel.objects.all()
    random_idea = IdeaSerializer(queryset[randint(0, len(queryset)-1)])
    async_to_sync(channel_layer.group_send)('random_idea', {'type': 'send_random_idea', 'text': random_idea})