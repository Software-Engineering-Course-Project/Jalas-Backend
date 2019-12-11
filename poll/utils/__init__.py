from poll.models import Poll, Select


def createSelect(poll_id, date, startTime, endTime):
    poll = Poll.objects.get(id=poll_id)
    select = Select(date=date, startTime=startTime, endTime=endTime, poll=poll)
    select.save()