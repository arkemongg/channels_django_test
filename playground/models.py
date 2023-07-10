from django.db import models
from django.conf import settings

# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def first_name(self):
        return self.user.first_name
    def last_name(self):
        return self.user.last_name
    
class Messages(models.Model):
    text = models.CharField(max_length=50)
    account = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    
    
