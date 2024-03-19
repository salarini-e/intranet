#This file is using channels daphne to consume the WebSocket
import json

from channels.generic.websocket import AsyncWebsocketConsumer

class OSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()

        # Add the consumer to a global group
        await self.channel_layer.group_add(
            'global_group',  # Use a global group name
            self.channel_name
        )

    async def disconnect(self, close_code):
        # Disconnect from the WebSocket
        await self.channel_layer.group_discard(
            'global_group',  # Use the same global group name
            self.channel_name
        )

    async def receive(self, text_data):
        # This method is called when the server receives a message from the WebSocket
        print("Received message:", text_data)

        # Broadcast the received message to all connected clients in the global group
        await self.channel_layer.group_send(
            'global_group',  # Use the same global group name
            {
                'type': 'chat.message',
                'message': text_data
            }
        )

    async def chat_message(self, event):
        # This method is called when the server receives a message from the global group
        message = event['message']

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({'message': message}))