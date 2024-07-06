import json
from channels.generic.websocket import AsyncWebsocketConsumer
<<<<<<< HEAD
from channels.db import database_sync_to_async
from app.models import Session, Recording

# Dictionary to store session data in memory
session_data = {}

class RecordingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs'].get('session_id')
        if not self.session_id:
            await self.close()
            return
        print(f"Connected to session: {self.session_id}")  # Debugging line
        await self.accept()

    async def disconnect(self, close_code):
        # On disconnect, save the recording data to the database
        if self.session_id in session_data:
            await self.save_session_data(self.session_id)
            del session_data[self.session_id]

    @database_sync_to_async
    def save_session_data(self, session_id):
        session, created = Session.objects.get_or_create(id=session_id)
        session.active = False
        session.save()
        Recording.objects.create(session=session, data=session_data[session_id])

    async def receive(self, text_data):
        data = json.loads(text_data)
        session_id = data.get('session_id', 'unknown')

        # Store session data in memory
        events = data.get('events', [])
        heatmap_data = session_data.get(session_id, [])

        for event in events:
            if event['type'] == 3 and 'x' in event['data'] and 'y' in event['data']:  # Ensure the event has coordinates
                x, y = event['data']['x'], event['data']['y']
                heatmap_data.append((x, y))

        # Store the heatmap data in the dictionary
        session_data[session_id] = heatmap_data
        print(f"Data for session {session_id}: {session_data[session_id]}")  # Debugging line

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
