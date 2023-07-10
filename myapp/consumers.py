from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
import json
from playground.models import Messages
from playground.serializers import MessageSerializer
from channels.db import database_sync_to_async
import requests
from django.http import HttpRequest
from rest_framework.renderers import JSONRenderer
from playground.views import MessageViewSet
from django.template.response import ContentNotRenderedError
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
        queryset = Messages.objects.filter(account_id = self.scope['user'].id).all()
        serializer = MessageSerializer(queryset, many=True)
        serialized_data = serializer.data
        return serialized_data
    @database_sync_to_async
    def database_post(self,message):
        
        queryset = Messages.objects.create(text=message,account_id = self.scope['user'].id)
        serializer = MessageSerializer(queryset)
        serialized_data = serializer.data
        return serialized_data

    async def all_message(self):
        queryset = await self.fetchfromviewset()
        print(queryset)
        last_message = await self.database()
        await self.send(json.dumps(queryset))


    @database_sync_to_async
    def fetchfromviewset(self):
                
        http_request = HttpRequest()
        http_request.method = 'GET'
        http_request.GET = self.scope['query_string'].decode()
        http_request.META = self.scope['headers']
        http_request.user = self.scope['user']

        # Instantiate the MessageViewSet with the HttpRequest
        viewset = MessageViewSet(request=http_request)

        # Call the desired method on the viewset
        response = viewset.list(request=viewset.request)
        try:
            response.renderer_context = {}
            response.accepted_media_type = 'application/json'
            response.accepted_renderer = JSONRenderer()
            response.render()
        except ContentNotRenderedError:
            pass

        # Retrieve the serialized data without OrderedDict objects
        data = json.loads(response.content)

        return data


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
        
        