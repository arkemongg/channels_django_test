from django.urls import path
from .consumers import (AsyncMyConsumer, GlobalConnectConsumer, GroupConsumer, GroupConsumerTest,
    HomePageConsumer, MyConsumer)

ws_url = [
    path('myapp/global/<string>',GlobalConnectConsumer.as_asgi()),
    path('myapp/test/<string>',MyConsumer.as_asgi()),
    path('myapp/asynctest/',AsyncMyConsumer.as_asgi()),
    path('myapp/groups/<int:pk>/<string>',GroupConsumer.as_asgi()),
    path('myapp/groups/test',GroupConsumerTest.as_asgi()),
    path('myapp/home/',HomePageConsumer.as_asgi())
]