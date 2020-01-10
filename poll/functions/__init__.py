import datetime

from django.utils import timezone


def check_poll_close(poll):
    if poll.status:
        return True
    if type(poll.date_close) != type(timezone.now()):
        time = datetime.datetime(poll.date_close.year, poll.date_close.month, poll.date_close.day)
    else:
        time = poll.date_close
    if poll.date_close:
        print(type(timezone.now()), type(poll.date_close))
        delta = timezone.now().timestamp() - time.timestamp()
        if delta > -1:
            poll.status = True
            poll.save()
            return True
    return False
