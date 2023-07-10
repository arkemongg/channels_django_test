from .models import Messages
from rest_framework import serializers

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ['text']
    def save(self, **kwargs):
        messages = Messages.objects.create(account_id = self.context['user_id'],**self.validated_data)
        messages.save()
        return super().save(**kwargs)
    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data