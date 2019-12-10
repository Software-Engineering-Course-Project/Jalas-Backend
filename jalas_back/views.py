import datetime
import json

import requests
from django.contrib.auth.models import User
from django.core import serializers
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from rest_framework.views import APIView

from Jalas import settings
from Jalas.settings import SITE_URL
from data_access.accress_logic import GetMeetings, GetPolls, GetSelects, SetReservationTimes, SetMeeting
from jalas_back.HttpResponces import HttpResponse400Error, HttpResponse404Error, HttpResponse500Error, \
    HttpResponse405Error
from jalas_back.Serializer import SelectSerializer
from jalas_back.models import Meeting, Poll, Select, ReservationTime


def test(request):
    ret = ''
    try:
        req = requests.get('http://213.233.176.40/available_rooms' +
        '?start=2019-11-30T12:30:00&end=2019-11-30T14:30:00')
        ret = req.json()
    except:
        return JsonResponse({"status": 10})
    return JsonResponse(ret)


class MeetingsView(APIView):
    def get(self, request):
        meetings = GetMeetings.all()
        meetings_json = serializers.serialize('json', meetings)
        return HttpResponse(meetings_json, content_type='application/json')


class PollsView(APIView):
    def get(self, request, meeting_id):
        polls = GetPolls.listByMeeting(meeting_id)
        polls_json = serializers.serialize('json', polls)
        return HttpResponse(polls_json, content_type='application/json')


class SelectsView(View):

    def get(self, request, poll_id):
        selects = GetSelects.listByPoll(poll_id)
        selects_json = SelectSerializer.makeSerial(selects)
        return HttpResponse(selects_json, content_type='application/json')


class RoomsView(APIView):
    def get(self, request, select_id):
        try:
            select = GetSelects.ById(select_id)
            try:
                req = requests.get(settings.API_ADDRESS + 'available_rooms' +
                                   '?start=' + str(select.date) + 'T' + str(select.startTime) +
                                   '&end=' + str(select.date) + 'T' + str(select.endTime))
                if req.status_code == 200:
                    return JsonResponse(req.json())
                else:
                    return HttpResponse500Error({
                        'Reservation system crash, please try again.'
                    })

            except:
                return HttpResponse500Error({
                    'Reservation system crash, please try again.'
                })
        except:
            return HttpResponse404Error({
                "This select id is not found."
            })


class SetDateView(APIView):
    def get(self, request, select_id):
        try:
            select = GetSelects.ById(select_id)
            meeting = select.poll.meeting
            meeting.startTime = select.startTime
            meeting.endTime = select.endTime
            meeting.date = select.date
            SetMeeting.save(meeting)
            SetReservationTimes.startTime(meeting.id)
            return HttpResponse("Set date and time successfully")
        except:
            return HttpResponse404Error({
                "select or poll not found"
            })


class SetRoomView(APIView):
    def get(self, request, room, select_id):
        try:
            select = GetSelects.ById(select_id)
            meeting = select.poll.meeting
            if meeting.room:
                return HttpResponse405Error({
                            "This meeting already set room"
                        })
            while True:
                try:
                    res = requests.post(url=settings.API_ADDRESS + 'rooms/'+ str(room) +'/reserve',
                                              json={
                                                  "username": 'rkhosravi',
                                                  "start": str(meeting.date) + 'T' + str(meeting.startTime),
                                                  "end": str(meeting.date) + 'T' + str(meeting.endTime),
                                              }
                                        )
                    select = GetSelects.ById(select_id)
                    meeting = select.poll.meeting
                    if meeting.isCancel:
                        meeting_json = serializers.serialize('json', [meeting])
                        return HttpResponse(meeting_json, content_type='application/json')

                    if res.status_code == 200:
                        meeting.room = room
                        meeting.status = 2
                        SetReservationTimes.endTime(meeting.id)
                        SetMeeting.save(meeting)
                        self.sendMail([meeting.owner.email, ], meeting)
                        meeting_json = serializers.serialize('json', [meeting])
                        return HttpResponse(meeting_json, content_type='application/json')
                    elif res.status_code == 400:
                        return HttpResponse404Error({
                            "Room Not found"
                        })
                except:
                    select = GetSelects.ById(select_id)
                    meeting = select.poll.meeting
                    if meeting.isCancel:
                        meeting_json = serializers.serialize('json', [meeting])
                        return HttpResponse(meeting_json, content_type='application/json')

        except:
            return HttpResponse404Error({
                "poll not found"
            })

    @staticmethod
    def sendMail(to, meeting):
        subject = meeting.title
        body = meeting.text
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, body, from_email, to, fail_silently=False)


class PollView(APIView):
    def get(self, request, poll_id):
        try:
            poll = GetPolls.ById(poll_id)
            poll_json = serializers.serialize('json', [poll])
            return HttpResponse(poll_json, content_type='application/json')
        except:
            return HttpResponse404Error({
                'this poll doesn\'t exist.'
            })


class SetCancel(APIView):
    def get(self, request, select_id):
        try:
            select = GetSelects.ById(select_id)
            meeting = select.poll.meeting
            meeting.isCancel = True
            meeting.status = 4
            meeting.room = None
            SetMeeting.save(meeting)
            SetReservationTimes.delete(meeting)
            meeting_json = serializers.serialize('json', [meeting])
            return HttpResponse(meeting_json, content_type='application/json')

        except:
            return HttpResponse404Error({
                'this select doesn\'t exist.'
            })


class ShowLogs(APIView):
    def get(self, request):
        overall_time = 0
        reservedRoomNum = 0
        reservatoinTimes = ReservationTime.objects.all()
        for reserve in reservatoinTimes:
            reservedRoomNum += 1
            start = reserve.reservationStartTime.strftime("%s")
            end = reserve.reservationEndTime.strftime("%s")
            end = int(end)
            start = int(start)
            overall_time += (end - start)
        overall_time = overall_time if overall_time > 0 else 0
        avg = overall_time / len(reservatoinTimes) if reservedRoomNum else 0
        canceledMeetings = GetMeetings.canceled()
        canceledNumber = len(canceledMeetings)
        res = "Till now: <br> Average time duration for each reservation is " + str(avg) + ' sec '+\
            "<br> " + 'Canceled meeting number is ' + str(canceledNumber) +\
            "<br>" + 'Reserved Room number is ' + str(reservedRoomNum)
        return HttpResponse(res)


class ShowMeeting(APIView):
    def get(self, request, select_id):
        try:
            select = GetSelects.ById(select_id)
            meeting = select.poll.meeting
            meeting_json = serializers.serialize('json', [meeting])
            return HttpResponse(meeting_json, content_type='application/json')
        except:
            return HttpResponse404Error(
                "This select_id doesn\'t exist."
            )


def test_send_email(request):
    send_mail('salam', 'jalas', settings.DEFAULT_FROM_EMAIL, ['mohammadhadi.omidi92@gmail.com',], fail_silently=False)
    return HttpResponse("ssss")


class CreatePoll(APIView):
    def post(self, request):
        title = request.GET['title']
        text = request.GET['text']
        user = User.objects.get(username='admin')
        meeting = Meeting(title=title, text=text, owner=user)
        meeting.save()
        poll = Poll(title=title, text=text, meeting=meeting)
        poll.save()
        poll_json = serializers.serialize('json', [poll])
        return HttpResponse(poll_json, content_type='application/json')

class CreateSelect(APIView):
    def post(self, request, poll_id):
        try:
            poll = Poll.objects.get(id=poll_id)
            date = request.GET['date']
            startTime = request.GET['start_time']
            endTime = request.GET['end_time']
            date = datetime.datetime.strptime(date, '%d-%m-%Y')
            startTime = datetime.datetime.strptime(startTime, '%H:%M:%S')
            endTime = datetime.datetime.strptime(endTime, '%H:%M:%S')
            select = Select(date=date, startTime=startTime, endTime=endTime, poll=poll)
            select.save()
            select_json = SelectSerializer.makeSerial([select])
            return HttpResponse(select_json, content_type='application/json')
        except:
            return HttpResponse404Error(
                "This poll doesn\'t exist."
            )
