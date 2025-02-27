from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(
        "ws/<str:room_id>/", consumers.MyConsumer.as_asgi()
    ),  
]
