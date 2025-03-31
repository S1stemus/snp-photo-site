import json

from channels.generic.websocket import AsyncWebsocketConsumer


class MyConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user_id = None
        self.group_name = None

    async def connect(self):
        if self.scope["user_id"]:
            self.user_id = f'user_{self.scope["user_id"]}'
            await self.channel_layer.group_add(self.user_id, self.channel_name)

        await self.channel_layer.group_add("users", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard("users", self.channel_name)
        if self.scope["user_id"]:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):

        await self.channel_layer.group_send(
            "users", {"type": "create", "message": text_data}
        )

    async def create(self, event):
        await self.send(text_data=json.dumps(event))
