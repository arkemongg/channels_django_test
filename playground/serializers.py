from .models import Messages
from rest_framework import serializers

class MessageSerailizers(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ['text']