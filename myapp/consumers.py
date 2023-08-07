from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
import json
from playground.models import Account, Groups, Messages
from playground.serializers import (GroupSerializer, MessageSerializer, SimpleGroupSerializer,
    SimpleMessageSerializer)
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
import requests
from django.http import HttpRequest
import rest_framework
from rest_framework.renderers import JSONRenderer
from playground.views import MessageViewSet
from django.template.response import ContentNotRenderedError
from asgiref.sync import async_to_sync
import requests

@database_sync_to_async
def jwt_verify(jwt_token):
    auth = requests.get("http://127.0.0.1:8000/auth/users/",headers={'Authorization': f'JWT {jwt_token}'})
    return auth
class GlobalConnectConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        jwt_token = self.scope['url_route']['kwargs']['string']
        self.group_id = "global"
        auth = await jwt_verify(jwt_token)
        if auth.status_code == 200:
            data = auth.json()
            self.scope["user"] = data
            await self.accept()
            my_groups =await self.my_group_db()
            await self.send_data("my_groups",my_groups )
            await self.channel_layer.group_add(self.group_id,self.channel_name)
        else:
            await self.close()
    
    async def receive(self, text_data):
        print(text_data)


    
    @database_sync_to_async
    def my_group_db(self):
        my_groups = Groups.objects.filter(accounts__id = self.scope['user'][0]["id"])
        serializer = SimpleGroupSerializer(my_groups,many=True)
        return serializer.data


    async def send_data(self,label,extra_data):
        data = {
            "label" : label,
            "data": extra_data
        }
        await self.send(json.dumps(data))    


class GroupConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        channel_layer = get_channel_layer()
        global_group = "global"
        self.group_id = str(self.scope['url_route']['kwargs']['pk'])

        jwt_token = self.scope['url_route']['kwargs']['string']
        auth = await jwt_verify(jwt_token)
        if auth.status_code == 200:
            data = auth.json()
            self.scope["user"] = data
        else:
            await self.close()


        if global_group in channel_layer.groups:
            if self.group_id in channel_layer.groups:
                 print(channel_layer.__dict__)
                 return

            await self.accept()

            data = await self.database()
            await self.send_data("connected",data)
            await self.channel_layer.group_add(self.group_id,self.channel_name)
        else:
            await self.close()
    
    async def receive(self, text_data):
        data = await self.save_message(text_data)
        await self.channel_layer.group_send(
            self.group_id,
            {
                'type':'chat.message',
                'data':data
            }
        )


    async def chat_message(self,event_data):
        print(event_data)
        await self.send_data('chat_message',event_data)    

    async def send_data(self,label,extra_data):
        data = {
            "label" : label,
            "data": extra_data
        }
        await self.send(json.dumps(data)) 


    @database_sync_to_async
    def save_message(self,text_data):
        account_id = self.scope['user'][0]['id']
        account = Account.objects.get(id = account_id)
        message = Messages.objects.create(account=account,text=text_data)
        group = Groups.objects.get(id=self.group_id)
        group.messages.add(message)
        message_serialized = SimpleMessageSerializer(message)
        return message_serialized.data
    
    @database_sync_to_async
    def database(self):
        group = Groups.objects.filter(id = int(self.group_id)).all()
        serializer = GroupSerializer(group,many=True)
        serialized_data = serializer.data
        ids = serialized_data[0]['messages']

        message = Messages.objects.filter(id__in=ids).values()
        message_serializer = MessageSerializer(message,many = True)
        serialized_data[0]['messages'] = message_serializer.data

        return serialized_data

 

class GroupConsumerTest(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        for i in range(10):
            print(i)
            await self.channel_layer.group_add(str(i), self.channel_name)
        layers = get_channel_layer()
        print(layers.__dict__)
    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.group_id,
            {
                'type': 'chat.message',
                'text': text_data,
                'user': self.scope['user'],
            }
        )
        
    async def chat_message(self, event):
        user = event['user']
        data = {
            'text_data': event['text'],
            'user': user.username,
        }
        await self.send(json.dumps(data))

    @database_sync_to_async
    def database(self):
        group = Groups.objects.filter(id = int(self.group_id)).all()
        serializer = GroupSerializer(group,many=True)
        serialized_data = serializer.data
        return serialized_data















class MyConsumer(WebsocketConsumer):
    def connect(self):
        jwt_token = self.scope['url_route']['kwargs']['string']
        x = requests.get("http://127.0.0.1:8000/auth/users/",headers={'Authorization': f'JWT {jwt_token}'})
        if x.status_code == 200:
            data = x.json()
            self.scope["user"] = data
            self.accept()
        else:
            self.close()
        self.send("ahsgda")  
    def receive(self, text_data):
        print(text_data)
   

class AsyncMyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.all_message()        

    @database_sync_to_async
    def database(self):
        queryset = Messages.objects.filter(account_id = self.scope['user'].id).all()
        serializer = MessageSerializer(queryset, many=True)
        serialized_data = serializer.data
        print(serialized_data)
        return serialized_data
    @database_sync_to_async
    def database_post(self,message):
        queryset = Messages.objects.create(text=message,account_id = self.scope['user'].id)
        serializer = MessageSerializer(queryset)
        serialized_data = serializer.data
        return serialized_data

    async def all_message(self):
        queryset = await self.fetchfromviewset()
        
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
        print(data)
        return data


    
    async def receive(self, text_data):
        data = await self.database_post(text_data)
        await self.send(json.dumps(data))



class HomePageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = "everyone"
        print(self.scope["user"])
        await self.accept()
        
        joined_groups = await self.groups_database_joined()
        await self.send_data("joined_groups",joined_groups)

        availabe_groups = await self.groups_database()
        await self.send_data("availabe_groups",availabe_groups)

        await self.channel_layer.group_add(self.group_id,self.channel_name)

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.group_id,
            {
                'type':'chat.message',
                'group_id':text_data,
            }
        )
    async def send_data(self,label,extra_data):
        data = {
            "label" : label,
            "data": extra_data
        }
        await self.send(json.dumps(data))

    async def chat_message(self,event):
        print(event)
        await self.send_data("updated_data",event)
    
    @database_sync_to_async
    def groups_database_joined(self):
        groups = Groups.objects.filter(accounts__id = self.scope["user"].id)
        serializer = SimpleGroupSerializer(groups,many = True)
        return serializer.data
    @database_sync_to_async
    def groups_database(self):
        groups = Groups.objects.exclude(accounts__id = self.scope["user"].id)
        serializer = SimpleGroupSerializer(groups,many = True)
        return serializer.data


