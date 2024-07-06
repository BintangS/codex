from django.urls import re_path

from . import socketHandler

websocket_urlpatterns = [
    re_path(r"ws/chat/$", socketHandler.ChatConsumer.as_asgi())
]