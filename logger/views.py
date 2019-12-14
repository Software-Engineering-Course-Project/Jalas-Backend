from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from logger.models import ReservationTime
from meeting.models import Meeting


class ShowLogs(APIView):
    def get(self, request):
        overall_time = 0
        reservedRoomNum = 0
        reservatoinTimes = ReservationTime.objects.all()
        for reserve in reservatoinTimes:
            reservedRoomNum += 1
            start = reserve.reservationStartTime.strftime("%s")
            end = reserve.reservationEndTime.strftime("%s")
            end = int(end) if end else None
            start = int(start) if start else None
            overall_time += (end - start) if (end != None and start != None) else 0
        overall_time = overall_time if overall_time > 0 else 0
        avg = overall_time / len(reservatoinTimes) if reservedRoomNum else 0
        canceledMeetings = Meeting.objects.filter(status=4)
        canceledNumber = len(canceledMeetings)
        res = "Till now: <br> Average time duration for each reservation is " + str(avg) + ' sec '+\
            "<br> " + 'Canceled meeting number is ' + str(canceledNumber) +\
            "<br>" + 'Reserved Room number is ' + str(reservedRoomNum)
        return HttpResponse(res)

