from django.utils import timezone

from logger.models import ReservationTime
from meeting.models import Meeting


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
