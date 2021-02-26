from channels.generic.websocket import AsyncJsonWebsocketConsumer
from idea.tasks import publish_most_recent_ideas
from idea_collector.celery import app

class GetMostRecent(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('most_recent', self.channel_name)
        await self.accept()
        publish_most_recent_ideas.delay()

    async def disconnect(self):
        await self.channel_layer.group_discard('most_recent', self.channel_name)

    async def send_most_recent(self, event):
        most_recent_ideas = [[idea.title, idea.description] for idea in event['text']]
        await self.send_json({'data': most_recent_ideas})
    
class GetRandomIdea(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('random_idea', self.channel_name)
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard('random_idea', self.channel_name)

    async def get_random_idea(self, event):
        random_idea = [event['text'].title, event['text'].description]
        await self.send_json({'data': random_idea})
