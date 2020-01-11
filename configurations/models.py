from authentication.models import User
from django.db import models

# Create your models here.


class Configuration(models.Model):
    arrange_meeting = models.BooleanField('arrange_meeting', default=False)
    create_poll = models.BooleanField('create_poll', default=False)
    add_option = models.BooleanField('add_option', default=False)
    new_vote = models.BooleanField('new_vote', default=False)
    remove_option = models.BooleanField('add_option', default=False)
    add_new_participant = models.BooleanField('add_new_participant', default=False)
    close_poll = models.BooleanField('close_poll', default=False)
    close_meeting = models.BooleanField('close_meeting', default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='configuration', default=None)
