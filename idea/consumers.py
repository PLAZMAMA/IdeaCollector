from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.consumer import SyncConsumer
from idea.tasks import publish_most_recent_ideas
from idea.serializers import IdeaSerializer
from idea.models import IdeaModel
from idea_collector.celery import app
from asgiref.sync import async_to_sync
from random import randint
from time import sleep

#uses the celery for its workers
class GetMostRecentIdea(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('most_recent', self.channel_name)
        await self.accept()
        publish_most_recent_ideas.delay()

    async def disconnect(self):
        await self.channel_layer.group_discard('most_recent', self.channel_name)

    async def send_most_recent_idea(self, event):
        most_recent_ideas = [[idea.title, idea.description] for idea in event['text']]
        await self.send_json({'data': most_recent_ideas})
    
#uses the celery for its workers
class GetRandomIdea(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('random_idea', self.channel_name)
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard('random_idea', self.channel_name)

    async def send_random_idea(self, event):
        random_idea = [event['text'].title, event['text'].description]
        await self.send_json({'data': random_idea})

#uses the built in channels worker for its workers
class GetMostRecentIdeasChannels(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('most_recent_channels', self.channel_name)
        await self.accept()
        await self.channel_layer.send('task-consumer', {'type': 'publish_most_recent_ideas'})

    async def disconnect(self):
        await self.channel_layer.group_discard('most_recent_channels', self.channel_name)

    async def send_most_recent(self, event):
        most_recent_ideas = [[idea.title, idea.description] for idea in event['text']]
        await self.send_json({'data': most_recent_ideas})
    
#uses the built in channels worker for its workers
class GetRandomIdeaChannels(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('random_idea_channels', self.channel_name)
        await self.accept()
        await self.get_random_idea()

    async def disconnect(self):
        await self.channel_layer.group_discard('random_idea_channels', self.channel_name)

    async def send_random_idea(self, event):
        random_idea = [event['text'].title, event['text'].description]
        await self.send_json({'data': random_idea})

    async def get_random_idea(self, sleep_time=5):
        while(True):
            sleep(sleep_time)
            await async_to_sync(self.channel_layer.send)('task-consumer', {'type': 'publish_random_idea'})

#used in the worker instance
class TaskConsumer(SyncConsumer):
    def publish_most_recent_ideas(self, num_of_ideas=5):
        queryset = IdeaModel.objects.all().order_by('-date_time')[:num_of_ideas]
        most_recent_ideas = IdeaSerializer(queryset, many=True)
        try:
            async_to_sync(self.channel_layer.group_send)('most_recent_channels', {'type': 'send_most_recent', 'text': most_recent_ideas})

        except Exception as e:
            sleep(5)
            async_to_sync(self.channel_layer.send)('task-consumer', {'type': 'publish_random_idea'})
            raise Exception(f'no one is connected to the websocket connection but just in case, the function is runing again(retry): {e}')

    def publish_random_idea(self):
        queryset = IdeaModel.objects.all()
        random_idea = IdeaSerializer(queryset[randint(0, len(queryset)-1)])
        async_to_sync(self.channel_layer.group_send)('random_idea_channels', {'type': 'send_random_idea', 'text': random_idea})