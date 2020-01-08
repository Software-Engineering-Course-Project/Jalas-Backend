from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from poll.models import Poll


class Comment(models.Model):
    owner = models.ForeignKey(User, related_name='comments', default=None, on_delete=models.CASCADE)
    text = models.TextField('متن')
    poll = models.ForeignKey(Poll, related_name='comments', on_delete=models.CASCADE, null=True, blank=True, default=None)
    parent = models.ForeignKey('Comment', related_name='replies', default=None, null=True, blank=True, on_delete=models.CASCADE)
    level = models.IntegerField('سطح', default=0)

    @property
    def get_replies(self):
        replies_list = []
        replies = self.replies.all()
        for rep in replies:
            replies_list.append(rep)
            replies_list += rep.get_replies
        return replies_list

    @property
    def get_poll(self):
        poll = self.poll
        if poll:
            return poll
        return self.parent.get_poll

    def can_delete(self, user):
        return (user == self.get_poll.meeting.owner) or (user == self.owner)

    def can_edit(self, user):
        return user == self.owner
