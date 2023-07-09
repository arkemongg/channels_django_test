from django.shortcuts import render
from django.http import HttpResponse
from .models import Messages
from .serializers import MessageSerailizers
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet

# Create your views here.
def hello(request):
    return render(request,'hello.html')

class MessageViewSet(ModelViewSet):

    serializer_class = MessageSerailizers
    
    def get_queryset(self):
        if self.request.method == 'GET':
            return Messages.objects.all()