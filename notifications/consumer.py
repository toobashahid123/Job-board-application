from channels.generic.websocket import AsyncWebsocketConsumer
import json



class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_id = self.scope['user'].id
        self.group_name = f"user_{user_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
        
        
        
        # class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Join a group
#         await self.channel_layer.group_add(
#             "notifications",
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave the group
#         await self.channel_layer.group_discard(
#             "notifications",
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         await self.send(text_data=json.dumps({
#             'message': data['message']
#         }))

#     async def send_notification(self, event):
#         # Send notification message to WebSocket clients
#         message = event['message']
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))    


