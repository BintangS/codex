import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Session, Recording

# Dictionary to store session data in memory
session_data = {}

class RecordingConsumer(AsyncWebsocketConsumer):
    DEFAULT_GROUP_NAME = 'codex'

    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs'].get('session_id')
        if not self.session_id:
            await self.close()
            return
        print(f"Connected to session: {self.session_id}")  # Debugging line

        # Add to group
        await self.channel_layer.group_add(self.DEFAULT_GROUP_NAME, self.channel_name)
        await self.accept()

        # create session in when socket is connected
        await self.create_session(self.session_id)

    async def disconnect(self, close_code):
        # On disconnect, save the recording data to the database
        if self.session_id in session_data:
            await self.save_session_data(self.session_id)
            del session_data[self.session_id]

        # Discard from group
        await self.channel_layer.group_discard(self.DEFAULT_GROUP_NAME, self.channel_name)

    @database_sync_to_async
    def create_session(self, session_id):
        return Session.objects.update_or_create(id=session_id, defaults={ 'active': True })

    @database_sync_to_async
    def save_session_data(self, session_id):
        session = Session.objects.get(id=session_id)
        session.active = False
        session.save()

        # save recording data to the database
        print(f"Saving data for session {session_id}: {session_data[session_id]}")
        Recording.objects.update_or_create(session=session, data=session_data[session_id])

    async def receive(self, text_data):
        data = json.loads(text_data)
        session_id = data.get('session_id', 'unknown')
        event_name = data.get('event_name')
        event_data = data.get('event_data')

        # Handle recording events
        if event_name == 'recording':
            events = event_data
            # heatmap_data = session_data.get(session_id, [])

            # comment out heatmap feature for now
            # for event in events:
            #     if event['type'] == 3 and 'x' in event['data'] and 'y' in event['data']:  # Ensure the event has coordinates
            #         x, y = event['data']['x'], event['data']['y']
            #         heatmap_data.append((x, y))

            # Store the heatmap data in the dictionary
            if session_id in session_data:
                session_data[session_id].append(events)
            else:
                session_data[session_id] = [events]

            # Broadcast the recording data to the group
            await self.channel_layer.group_send(self.DEFAULT_GROUP_NAME, {
                'type': 'livestream', # this will call the "livestream" method
                'text': json.dumps({
                    'event': 'livestream-data',
                    'data': event_data
                })
            })

        elif event_name == 'view-livestream':
            # Additional logic for subscribing to the livestream group if needed
            pass

    async def livestream(self, event):
        await self.send(text_data=event["text"])