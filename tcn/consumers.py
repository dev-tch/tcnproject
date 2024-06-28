from channels.generic.websocket import AsyncWebsocketConsumer
import json

class CounterConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('counter_group', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('counter_group', self.channel_name)

    async def counter_update(self, event):
        await self.send(text_data=json.dumps({
            'counter': event['counter']
        }))
