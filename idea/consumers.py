from channels.generic.websocket import AsyncWebsockerConsumer

class GetMostRecent(AsyncWebsockerConsumer):
    async def connect(self):
        await self.channel_layer.group_add('most_recent', self.channel_name)
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard('most_recent', self.channel_name)

    async def get_most_recent(self):
        