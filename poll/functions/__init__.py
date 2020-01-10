from django.utils import timezone


def check_poll_close(poll):
    if poll.status:
        return True
    if poll.date_close:
        print(type(timezone.now()), type(poll.date_close))
        delta = timezone.now().timestamp() - poll.date_close.timestamp()
        if delta > -1:
            poll.status = True
            poll.save()
            return True
    return False
