from celery import shared_task
from idea.models import IdeaModel
from idea.views import IdeaViewSet
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
        async_to_sync(channel_layer.group_send)('most_recent', {'type': 'get_most_recent', 'text': most_recent_ideas})

    except Exception as e:
        raise Exception(f'no one is connected to the websocket connection but just in case, the function will run again(retry) in 5 seconds: {e}', countdown=5)

@shared_task
def get_random_idea():
    ideas = IdeaView.list()
    random_idea = ideas[randint(0, len(ideas)-1)]
    async_to_sync(channel_layer.group_send)('random_idea', {'type': 'get_random_idea', 'text': random_idea})