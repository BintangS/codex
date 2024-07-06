import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RecordingConsumer(AsyncWebsocketConsumer):
    DEFAULT_GROUP_NAME = 'codex'

    async def connect(self):
        await self.channel_layer.group_add(self.DEFAULT_GROUP_NAME, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.DEFAULT_GROUP_NAME, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)

        event_name = data.get('event_name')
        event_data = data.get('event_data')
        
        if event_name == 'recording':
            # Process the received data here (e.g., save to database)
            await self.channel_layer.group_send(self.DEFAULT_GROUP_NAME, {
                'type': 'livestream',
                'text': json.dumps({
                    'event': 'livestream-data',
                    'data': event_data
                })
            })
        elif event_name == 'view-livestream':
            # subscribe to the livestream group
            pass

    async def livestream(self, event):
        await self.send(text_data=event["text"])