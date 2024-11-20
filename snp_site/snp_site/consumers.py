import json
from channels.generic.websocket import WebsocketConsumer

class MyConsumer(WebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'message': 'Welcome to the WebSocket server!'
        }))

    async def disconnect(self, close_code):
        pass  # Здесь можно обработать отключение

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')

        # Отправка обратно клиенту
        await self.send(text_data=json.dumps({
            'message': message
        }))