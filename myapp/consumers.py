from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
import json
from playground.models import Messages
from playground.serializers import MessageSerailizers
from channels.db import database_sync_to_async
class MyConsumer(WebsocketConsumer):
    groups = ["broadcast"]
    
    def connect(self):
        self.accept()
        queryset = Messages.objects.all()
        
        self.send(queryset[-1].text)
        
        

    def receive(self, text_data):
        print(text_data)
class AsyncMyConsumer(AsyncWebsocketConsumer):
    groups = ["broadcast"]

    @database_sync_to_async
    def database(self):
        queryset = Messages.objects.all()
        serializer = MessageSerailizers(queryset, many=True)
        serialized_data = serializer.data
        return serialized_data
    @database_sync_to_async
    def database_post(self,message):
        queryset = Messages.objects.create(text=message)
        serializer = MessageSerailizers(queryset)
        serialized_data = serializer.data
        return serialized_data

    async def all_message(self):
        last_message = await self.database()
        await self.send(json.dumps(last_message))


    # async def send_last_message(self):
    #     last_message = await self.database()
    #     print("lastmessage called")
    #     await self.send(json.dumps(last_message))
            

    async def connect(self):
        await self.accept()
        await self.all_message()
    
    async def receive(self, text_data):
        data = await self.database_post(text_data)
        await self.send(json.dumps(data))
        
        