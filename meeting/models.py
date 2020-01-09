from authentication.models import User
from django.db import models

# Create your models here.

class Meeting(models.Model):
    MEET_STATUS = (
        (1, 'در انتظار اتاق'),
        (2, 'رزرو کامل'),
        (3, 'برگزار شده'),
        (4, 'لغو شده'),
    )
    title = models.CharField('عنوان', max_length=100)
    text = models.TextField('متن')
    owner = models.ForeignKey(User, related_name='meetings', null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateField(verbose_name='تاریخ', null=True, blank=True, default=None)
    startTime = models.TimeField(verbose_name='زمان شروع', null=True, blank=True, default=None)
    endTime = models.TimeField(verbose_name='زمان اتمام', null=True, blank=True, default=None)
    status = models.IntegerField(choices=MEET_STATUS, verbose_name='وضعیت جلسه', null=True, blank=True, default=1)
    room = models.IntegerField(verbose_name='شماره اتاق', null=True, blank=True, default=None)
    isCancel = models.BooleanField(verbose_name='وضعیت لغو', default=False, blank=True)
