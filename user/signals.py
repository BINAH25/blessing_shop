from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from dashboard.models import *
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    print("DEBUf", created,instance.user_type)
    if created:
        if instance.user_type==1:
            AdminHEAD.objects.create(admin=instance)
        if instance.user_type==2:
            Customer.objects.create(admin=instance)
        
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if instance.user_type==1:
        instance.adminhead.save()
    if instance.user_type==2:
        instance.customer.save()
    