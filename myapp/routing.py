from django.urls import path
from .consumers import MyConsumer,AsyncMyConsumer

ws_url = [
    path('myapp/test/',MyConsumer.as_asgi()),
    path('myapp/asynctest/',AsyncMyConsumer.as_asgi())
]