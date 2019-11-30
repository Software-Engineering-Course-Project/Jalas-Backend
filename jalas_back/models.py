from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Meeting(models.Model):
    MEET_STATUS = (
        (1, 'در انتظار اتاق'),
        (2, 'رزرو کامل'),
        (3, 'برگزار شده'),
    )
    title = models.CharField('عنوان', max_length=100)
    text = models.TextField('متن')
    owner = models.ForeignKey(User, related_name='meetings', null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateField(verbose_name='تاریخ', null=True, blank=True, default=None)
    startTime = models.TimeField(verbose_name='زمان شروع', null=True, blank=True, default=None)
    endTime = models.TimeField(verbose_name='زمان اتمام', null=True, blank=True, default=None)
    status = models.IntegerField(choices=MEET_STATUS, verbose_name='وضعیت جلسه', null=True, blank=True, default=None)


class MeetingParticipant(models.Model):
    participant = models.ForeignKey(User, related_name='participateIn', null=True, blank=True, on_delete=models.SET_NULL)
    meeting = models.ForeignKey(Meeting, related_name='participants', null=True, blank=True, on_delete=models.SET_NULL)


class Poll(models.Model):
    title = models.CharField('عنوان', max_length=100)
    text = models.TextField('متن')
    meeting = models.ForeignKey(Meeting, related_name='polls', on_delete=models.CASCADE)


class Select(models.Model):
    text = models.TextField('متن', null=True, blank=True)
    poll = models.ForeignKey(Poll, related_name='selects', on_delete=models.CASCADE, default=None)

    @property
    def getDisagreeNumber(self):
        count = 0
        for vote in self.voted.all():
            if vote.agreement == 1:
                count += 1
        return count

    @property
    def getAgreeNumber(self):
        count = 0
        for vote in self.voted.all():
            if vote.agreement == 2:
                count += 1
        return count

    agree = getAgreeNumber
    disAgree = getDisagreeNumber



class SelectUser(models.Model):
    AGGREMENT_CHOICE = (
        (1, 'خیر'),
        (2, 'بله')
    )
    user = models.ForeignKey(User, related_name='voted', null=True, blank=True, on_delete=models.SET_NULL)
    select = models.ForeignKey(Select, related_name='voted', null=True, blank=True, on_delete=models.SET_NULL)
    agreement = models.IntegerField(verbose_name='نظر', null=True, choices=AGGREMENT_CHOICE)

