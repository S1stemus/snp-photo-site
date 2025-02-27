import json
from channels.generic.websocket import AsyncWebsocketConsumer


class MyConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_id = None
        self.group_name = None

    async def connect(self):
        # Code to run when the WebSocket is handshaking as part of the connection process.
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        print('roomid', self.room_id)
        self.group_name = self.room_id
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Code to run when the WebSocket closes for any reason.
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # Code to run when the server receives a message from the WebSocket.
        await self.channel_layer.group_send(
            self.group_name, {
                'type': 'create',
                'message': text_data
            })

    async def create(self, event):
        # Code to run when the server send message to the WebSocket.
        await self.send(text_data=json.dumps(event))