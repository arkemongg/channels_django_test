from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save
from django.conf import settings
from playground.models import Account

@receiver(post_save,sender = settings.AUTH_USER_MODEL)
def create_account_when_create_user(sender,**kwargs):
    if kwargs['created']:
        print(kwargs)
        account = Account.objects.create(user = kwargs['instance'])
        account.save()

