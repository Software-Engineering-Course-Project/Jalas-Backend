from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from authentication import models
from configurations.models import Configuration


@receiver(post_save, sender=models.User)
def save_user_profile(sender, instance, **kwargs):
    conf = Configuration(user=instance)
    conf.save()
    instance.configuration = conf
