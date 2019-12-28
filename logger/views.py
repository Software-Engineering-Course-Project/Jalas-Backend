import time

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from logger.models import ReservationTime, Response, Throughput
from meeting.models import Meeting

class ShowLogs(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.username == 'admin':
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
            avg_res_time = self.getAverageResponseTime()
            throughput = self.get_throughput()

            res = "Till now: <br> Average time duration for each reservation is " + str(avg) + ' sec '+\
                "<br> " + 'Canceled meeting number is ' + str(canceledNumber) +\
                "<br>" + 'Reserved Room number is ' + str(reservedRoomNum) +\
                "<br>" + ('Average response time is %2.4f' % avg_res_time) +\
                '<br>' + 'Throughput is ' + str(throughput)
            return HttpResponse(res)
        return HttpResponse('You can\'t see logs.')

    def getAverageResponseTime(self):
        res_times = Response.objects.all()
        s = 0.0
        for res_time in res_times:
            s += res_time.duration
        return s / (len(res_times) if len(res_times) else 1)

    def get_throughput(self):
        this_time = time.time()
        throughput_time = 1.0 * 60 * 5
        tp = Throughput.objects.filter(create_date__gte=(this_time - throughput_time))
        return len(tp)