from django.db import models

# Create your models here.
from meeting.models import Meeting


class ReservationTime(models.Model):
    reservationStartTime = models.TimeField(verbose_name='زمان شروع', null=True, blank=True, default=None)
    reservationEndTime = models.TimeField(verbose_name='زمان پایان', null=True, blank=True, default=None)
    meeting = models.ForeignKey(Meeting, related_name='reserveDuration', on_delete=models.SET_NULL, null=True)