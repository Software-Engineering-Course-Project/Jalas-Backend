from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone

from meeting.models import Meeting


class MeetingParticipant(models.Model):
    participant = models.ForeignKey(User, related_name='participateIn', on_delete=models.CASCADE, default=None)
    meeting = models.ForeignKey(Meeting, related_name='participants', on_delete=models.CASCADE, default=None)


class Poll(models.Model):
    title = models.CharField('عنوان', max_length=100)
    text = models.TextField('متن')
    meeting = models.ForeignKey(Meeting, related_name='polls', on_delete=models.CASCADE)


class Select(models.Model):
    date = models.DateField(verbose_name='تاریخ', default=timezone.now)
    startTime = models.TimeField(verbose_name='زمان شروع', default=timezone.now)
    endTime = models.TimeField(verbose_name='زمان اتمام', default=timezone.now)
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

    @property
    def getIfNeededNumber(self):
        count = 0
        for vote in self.voted.all():
            if vote.agreement == 3:
                count += 1
        return count

    agree = getAgreeNumber
    disagree = getDisagreeNumber
    ifNeeded = getIfNeededNumber



class SelectUser(models.Model):
    AGGREMENT_CHOICE = (
        (1, 'خیر'),
        (2, 'بله'),
        (3, 'اگر مجبور بودم می‌آیم')
    )
    user = models.ForeignKey(User, related_name='voted', default=None, on_delete=models.CASCADE)
    select = models.ForeignKey(Select, related_name='voted', default=None, on_delete=models.CASCADE)
    agreement = models.IntegerField(verbose_name='نظر', null=True, choices=AGGREMENT_CHOICE)
    name = models.CharField(verbose_name='نام شرکت کننده', max_length=100, default=None)
