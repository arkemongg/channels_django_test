from rest_framework import serializers

from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer ,TokenCreateSerializer as BaseTokenCreateSerializer


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['email','username','password','first_name','last_name']
class TokenCreateSerializer(BaseTokenCreateSerializer):
    pass

# {
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4ODk5ODgwNCwiaWF0IjoxNjg4OTEyNDA0LCJqdGkiOiI3NGM2ODNjNzZhMTc0ZTJhYjYxYzgwYjVhZDAzMDk5OSIsInVzZXJfaWQiOjF9.UsEQLMGgmAdy3pOSlyKdzBanTheaIKdPySZoDw9WJVg",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg4OTk4ODA0LCJpYXQiOjE2ODg5MTI0MDQsImp0aSI6IjVjNGFhMDUwYmMzZDRkY2ZiMWFkM2ViOTBjMWVlYjhiIiwidXNlcl9pZCI6MX0.zzFMGi9J1SnAA-HRQUxAX153CiOB1F7R5AZAgkxPOSI"
# }