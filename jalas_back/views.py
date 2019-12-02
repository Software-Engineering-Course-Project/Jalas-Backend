import json

import requests
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
from jalas_back.HttpResponces import HttpResponse400Error, HttpResponse404Error, HttpResponse500Error
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

    # def post(self, request):
    #     select_id = int(request.POST['select_id'])
    #     select = Select.objects.filter(id=select_id)
    #     if select:
    #         select = select[0]
    #         meeting = select.poll.meeting
    #         meeting.date = select.date
    #         meeting.startTime = meeting.startTime
    #         meeting.endTime = meeting.endTime
    #         SetMeeting.save(meeting)
    #         return JsonResponse({"status": 200,
    #                              "text": 'Meeting set up.'
    #                              })
    #     return JsonResponse({"status": 100,
    #                          "text": 'Meeting doesn\'t exist.'})

#
# def getMeeting(request):
#     meetings = Meeting.objects.all()
#     meetings_json = serializers.serialize('json', meetings)
#     return HttpResponse(meetings_json, content_type='application/json')


class PollsView(APIView):
    def get(self, request, meeting_id):
        polls = GetPolls.listByMeeting(meeting_id)
        polls_json = serializers.serialize('json', polls)
        return HttpResponse(polls_json, content_type='application/json')


# def getPolls(request, meeting_id):
#     polls = Poll.objects.filter(meeting_id=meeting_id)
#     polls_json = serializers.serialize('json', polls)
#     return HttpResponse(polls_json, content_type='application/json')


class SelectsView(View):

    def get(self, request, poll_id):
        selects = GetSelects.listByPoll(poll_id)
        selects_json = SelectSerializer.makeSerial(selects)
        return HttpResponse(selects_json, content_type='application/json')

# def getSelect(request, poll_id):
#     selects = Select.objects.filter(poll_id=poll_id)
#     selects_json = SelectSerializer.makeSerial(selects)
#     return HttpResponse(selects_json, content_type='application/json')


# def setMeetingTime(request, select_id):
#     select = Select.objects.filter(id=select_id)
#     if select:
#         select = select[0]
#         meeting = select.poll.meeting
#         meeting.date = select.date
#         meeting.startTime = meeting.startTime
#         meeting.endTime = meeting.endTime
#         SetMeeting.save(meeting)
#         return redirect(SITE_URL + 'api/available_room/' + str(meeting.id))
#     return JsonResponse({"status": 100})


class RoomsView(APIView):
    def get(self, request, select_id):
        try:
            select = GetSelects.ById(select_id)
            try:
                req = requests.get('http://213.233.176.40/available_rooms' +
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
                return HttpResponse({
                            "This meeting already set room"
                        })
            while True:
                try:
                    res = requests.post(url='http://213.233.176.40/rooms/'+ str(room) +'/reserve',
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

    #
    # def post(self, request, select_id):
    #     try:
    #         select_id = int(request.POST['select_id'])
    #         room_number = int(request.POST['room_number'])
    #         select = None
    #         try:
    #             select = Select.objects.get(id=select_id)
    #         except:
    #             JsonResponse({
    #                 "status": 100,
    #                 "text": 'There is no this select id.'
    #             })
    #         meeting = select.poll.meeting
    #         if meeting:
    #             if meeting.room:
    #                 # status = 91 means that this meeting has a room.
    #                 return JsonResponse({
    #                     "status": 91,
    #                     "text": 'This meeting has a room.'
    #                 })
    #             req = requests.get('http://213.233.176.40/available_rooms' +
    #                                '?start=' + str(meeting.date) + 'T' + str(meeting.startTime) +
    #                                '&end=' + str(meeting.date) + 'T' + str(meeting.endTime))
    #             availableRooms = req.json()['availableRooms']
    #             if room_number not in availableRooms:
    #                 # status = 90 means that this room has been reserved when you want to reserve it.
    #                 return JsonResponse({"status": 90,
    #                                      "text": 'This room reserved when you want to reserve it.'})
    #             meeting.room = room_number
    #             meeting.status = 2
    #             SetMeeting.save(meeting)
    #             res = requests.post(url='http://213.233.176.40/rooms/210/reserve',
    #                           data={
    #                               "username": 'mh.omidi',
    #                               "start": str(meeting.date) + 'T' + str(meeting.startTime),
    #                               "end": str(meeting.date) + 'T' + str(meeting.endTime),
    #                           }
    #                     )
    #             # print(str(meeting.date) + 'T' + str(meeting.startTime))
    #             # print(str(meeting.date) + 'T' + str(meeting.endTime))
    #             # print(str(res.json()))
    #             return JsonResponse({
    #                 "status": 200,
    #                 "text": 'Room reserved successfully'
    #
    #             })
    #         # status = 100 means that this meeting doesn't exist.
    #         return JsonResponse({"status": 100,
    #                              "text": "Meeting doesn\'t exist."
    #                              })
    #     except:
    #         return JsonResponse({"status": 0,
    #                              "text": 'An Exception occure, please try again.'})

# def getAvailaibleRoom(request, meeting_id):
#     meeting = Meeting.objects.filter(id=meeting_id)
#     if meeting:
#         meeting = meeting[0]
#         if not meeting.date or meeting.endTime or meeting.startTime:
#             # status = 100 means that this meeting doesn't exist.
#             return JsonResponse({"status": 100})
#         req = requests.get('http://213.233.176.40/available_rooms' +
#                            '?start=' + str(meeting.date) + 'T' + str(meeting.startTime) +
#                            '&end=' + str(meeting.date) + 'T' + str(meeting.endTime))
#         return HttpResponse(str(req.json()))
#     # status = 100 means that this meeting doesn't exist.
#     return JsonResponse({"status": 100})


# def setMeetingRoom(request, meeting_id, room_number):
#     meeting = Meeting.objects.filter(id=meeting_id)
#     if meeting:
#         meeting = meeting[0]
#         if meeting.room:
#             # status = 91 means that this meeting has a room.
#             return HttpResponse('{"status" : 91}')
#         req = requests.get('http://213.233.176.40/available_rooms' +
#                            '?start=' + str(meeting.date) + 'T' + str(meeting.startTime) +
#                            '&end=' + str(meeting.date) + 'T' + str(meeting.endTime))
#         availableRooms = req.json()['availableRooms']
#         if room_number not in availableRooms:
#             # status = 90 means that this room has been reserved when you want to reserve it.
#             return HttpResponse('{"status" : 90}')
#         meeting.room = room_number
#         meeting.status = 2
#         SetMeeting.save(meeting)
#         return redirect(SITE_URL + 'api/show_meeting/' + str(meeting_id))
#     # status = 100 means that this meeting doesn't exist.
#     return JsonResponse({"status": 100})

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
        avg = overall_time / len(reservatoinTimes) if reservedRoomNum else 0
        canceledMeetings = GetMeetings.canceled()
        canceledNumber = len(canceledMeetings)
        res = "Till now: <br> Average time duration for each reservation is " + str(avg) + ' sec '+\
            "<br> " + 'Canceled meeting number is ' + str(canceledNumber) +\
            "<br>" + 'Reserved Room number is ' + str(reservedRoomNum)
        return HttpResponse(res)


def showMeeting(request, select_id):
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