from django.urls import path,include
from .views import hello, MessageViewSet

from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register('messages',MessageViewSet,basename='message-list')
urlpatterns = [
    path('hello/',hello),
    path('', include(router.urls)),
]
