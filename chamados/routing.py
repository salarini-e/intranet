
from django.urls import path

from . import consumers

websocket_urlspatters = [
    path("ws/", consumers.OSConsumer.as_asgi())
]
