from django.utils import timezone

from jalas_back.models import Select, Poll, Meeting, ReservationTime


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

    @staticmethod
    def canceled():
        return Meeting.objects.filter(status=4)

class SetReservationTimes:
    @staticmethod
    def startTime(meeting_id):
        try:
            meeting = Meeting.objects.get(id=meeting_id)
            try:
                reserveTime = ReservationTime.objects.get(meeting=meeting)
                reserveTime.reservationStartTime = timezone.now()
                reserveTime.save()
            except:
                reserveTime = ReservationTime(meeting=meeting, reservationStartTime=timezone.now())
                reserveTime.save()
        except:
            pass


    @staticmethod
    def endTime(meeting_id):
        try:
            meeting = Meeting.objects.get(id=meeting_id)
            try:
                reserveTime = ReservationTime.objects.get(meeting=meeting)
                reserveTime.reservationEndTime = timezone.now()
                reserveTime.save()
            except:
                reserveTime = ReservationTime(meeting=meeting, reservationEndTime=timezone.now())
                reserveTime.save()
        except:
            pass

    @staticmethod
    def delete(meeting):
        try:
            reserveTime = ReservationTime.objects.get(meeting=meeting)
            reserveTime.delete()
        except:
            pass

class SetMeeting:
    @staticmethod
    def save(meeting):
        meeting.save()
