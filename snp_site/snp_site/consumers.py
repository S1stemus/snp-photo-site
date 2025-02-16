import json

from channels.generic.websocket import WebsocketConsumer


class MyConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print("WebSocket connected")
        self.send(json.dumps({"message": "Welcome to the WebSocket server!"}))
