from channels.generic.websocket import AsyncWebsockerConsumer
from idea_collector.celery import app

class GetMostRecent(AsyncWebsockerConsumer):
    async def connect(self):
        await self.channel_layer.group_add('most_recent', self.channel_name)
        await self.accept()
        await self.get_most_recent()
        

    async def disconnect(self):
        await self.channel_layer.group_discard('most_recent', self.channel_name)

    async def get_most_recent(self):


    async def send_most_recent(self, event):
        ideas = [[idea.title, idea.description] for idea in event['text']]
        await self.send(ideas)
        