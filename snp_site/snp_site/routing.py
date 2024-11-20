from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path('ws/api/', consumers.MyConsumer.as_asgi()),  # Укажите путь для WebSocket
]