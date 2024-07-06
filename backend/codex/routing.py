from django.urls import re_path


from . import socketHandler
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/$", socketHandler.ChatConsumer.as_asgi()),
    re_path(r'ws/recordings/(?P<session_id>[^/]+)/$', consumers.RecordingConsumer.as_asgi()),
]