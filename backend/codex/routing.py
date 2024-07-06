from django.urls import re_path

<<<<<<< HEAD

from . import socketHandler
from . import consumers
websocket_urlpatterns = [
    re_path(r"ws/chat/$", socketHandler.ChatConsumer.as_asgi()),
    re_path(r'ws/recordings/(?P<session_id>[^/]+)/$', consumers.RecordingConsumer.as_asgi()),
=======
from . import consumers
websocket_urlpatterns = [
    re_path(r"ws/recordings/", consumers.RecordingConsumer.as_asgi()),
>>>>>>> master
]