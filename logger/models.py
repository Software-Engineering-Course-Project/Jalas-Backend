from django.db import models

# Create your models here.
from django.utils import timezone

from meeting.models import Meeting


class ReservationTime(models.Model):
    reservationStartTime = models.TimeField(verbose_name='زمان شروع', null=True, blank=True, default=None)
    reservationEndTime = models.TimeField(verbose_name='زمان پایان', null=True, blank=True, default=None)
    meeting = models.ForeignKey(Meeting, related_name='reserveDuration', on_delete=models.SET_NULL, null=True)


class Throughput(models.Model):
    create_date = models.DateField(default=timezone.now)


class Response(models.Model):
    duration = models.FloatField(default=0.0)