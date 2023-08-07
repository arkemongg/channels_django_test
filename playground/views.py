from django.shortcuts import render
from django.http import HttpResponse
from core.models import User
from .models import Messages
from .serializers import MessageSerializer
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# Create your views here.
def hello(request):
    return render(request,'hello.html')

class MessageViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        if self.request.method == 'GET':
            print(self.request.user)
            return Messages.objects.filter(account_id=self.request.user.id).all()
    def get_serializer_context(self):
        return {
            'user_id':self.request.user.id
        }
# {
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4OTA4NTg5MCwiaWF0IjoxNjg4OTk5NDkwLCJqdGkiOiI3ZTU2MTY2ZTI1MDM0ZjI0OGJhZjUwZTY4ZTQ0ZmE2MSIsInVzZXJfaWQiOjF9.4jQJ56Xtjy7n9EM23IC90ZRVBmFzC4cFtg0FSQbVw2M",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg5MDg1ODkwLCJpYXQiOjE2ODg5OTk0OTAsImp0aSI6ImM1YWMyYjk5NTY1NjQ3ZmQ5NGMyYTcwYzAxMTBhMmM3IiwidXNlcl9pZCI6MX0.tJw9gxWFfO7h5t6ws9CGMQoNDvEfQwAwLo5KpVGUjvQ"
# }