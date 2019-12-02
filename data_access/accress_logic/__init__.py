from jalas_back.models import Select, Poll, Meeting


class GetSelects:
    @staticmethod
    def ById(select_id):
        try:
            return Select.objects.get(id=select_id)
        except:
            return None


    @staticmethod
    def listByPoll(poll_id):
        return Select.objects.filter(poll_id=poll_id)

    @staticmethod
    def all():
        return Select.objects.all()




class GetPolls:
    @staticmethod
    def ById(poll_id):
        try:
            return Poll.objects.get(id=poll_id)
        except:
            return None


    @staticmethod
    def listByMeeting(meeting_id):
        return Poll.objects.filter(meeting_id=meeting_id)

    @staticmethod
    def all():
        return Poll.objects.all()




class GetMeetings:
    @staticmethod
    def ById(meeting_id):
        try:
            return Meeting.objects.get(id=meeting_id)
        except:
            return None


    @staticmethod
    def listByUser(user_id):
        return Meeting.objects.filter(user_id=user_id)

    @staticmethod
    def all():
        return Meeting.objects.all()
