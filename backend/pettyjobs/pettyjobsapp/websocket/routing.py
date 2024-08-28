from django.urls import path
from .consumers import testConsumer,JobConsumer
websocket_patterns = [
    path('ws/test/',testConsumer.as_asgi()),
    path('ws/jobs/',JobConsumer.as_asgi()),
]