from django.db import models

# Create your models here.

class Users(models.Model):
    pass

class Messages(models.Model):
    text = models.CharField(max_length=50)
    
    
