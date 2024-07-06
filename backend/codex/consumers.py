import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RecordingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Process the received data here (e.g., save to database)
        print(data)