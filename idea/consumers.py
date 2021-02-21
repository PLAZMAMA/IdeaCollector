from channels.generic.websocket import AsyncWebsockerConsumer
from idea.tasks import publish_most_recent_ideas

class GetMostRecent(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('most_recent', self.channel_name)
        await self.accept()
        publish_most_recent_ideas.delay()

    async def disconnect(self):
        await self.channel_layer.group_discard('most_recent', self.channel_name)

    async def send_most_recent(self, event):
        ideas = [[idea.title, idea.description] for idea in event['text']]
        await self.send(ideas)
        