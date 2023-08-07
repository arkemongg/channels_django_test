from .models import Groups, Messages,Account
from rest_framework import serializers

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'user', 'joined_groups', 'first_name', 'last_name']
        read_only_fields = ['first_name', 'last_name']

class SimpleMessageSerializer(serializers.ModelSerializer):
    account_name = serializers.SerializerMethodField()
    class Meta:
        model = Messages
        fields = ['account_name','id', 'text','account_id', 'created_at']

    def get_account_name(self, obj):
        account_id = obj.account_id
        try:
            account = Account.objects.get(id=account_id)
            full_name = f"{account.user.first_name} {account.user.last_name}"
            return full_name
        except Account.DoesNotExist:
            return None
class MessageSerializer(serializers.ModelSerializer):
    account_name = serializers.SerializerMethodField()
    class Meta:
        model = Messages
        fields = ['account_name','id', 'text','account_id', 'created_at']

    def get_account_name(self, obj):
        account_id = obj.get('account_id')
        try:
            account = Account.objects.get(id=account_id)
            full_name = f"{account.user.first_name} {account.user.last_name}"
            return full_name
        except Account.DoesNotExist:
            return None

    def save(self, **kwargs):
        account = Account.objects.get(id = self.context['user_id'])
        messages = Messages.objects.create(account = account,**self.validated_data)
        messages.save()
        return super().save(**kwargs)
    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     return data
    
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = ['id','title','messages','accounts']

class SimpleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = ['id','title','members']

    members = serializers.SerializerMethodField()

    def get_members(self,obj):
        account = Groups.objects.get(id = obj.id)
        return account.accounts.all().count()

