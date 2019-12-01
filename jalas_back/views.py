import json

import requests
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from rest_framework.views import APIView

from Jalas.settings import SITE_URL
from jalas_back.Serializer import SelectSerializer
from jalas_back.models import Meeting, Poll, Select


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
        meetings = Meeting.objects.all()
        meetings_json = serializers.serialize('json', meetings)
        return HttpResponse(meetings_json, content_type='application/json')

    def post(self, request):
        select_id = int(request.POST['select_id'])
        select = Select.objects.filter(id=select_id)
        if select:
            select = select[0]
            meeting = select.poll.meeting
            meeting.date = select.date
            meeting.startTime = meeting.startTime
            meeting.endTime = meeting.endTime
            meeting.save()
            return JsonResponse({"status": 200,
                                 "text": 'Meeting set up.'
                                 })
        return JsonResponse({"status": 100,
                             "text": 'Meeting doesn\'t exist.'})

#
# def getMeeting(request):
#     meetings = Meeting.objects.all()
#     meetings_json = serializers.serialize('json', meetings)
#     return HttpResponse(meetings_json, content_type='application/json')


class PollsView(APIView):
    def get(self, request, meeting_id):
        polls = Poll.objects.filter(meeting_id=meeting_id)
        polls_json = serializers.serialize('json', polls)
        return HttpResponse(polls_json, content_type='application/json')


# def getPolls(request, meeting_id):
#     polls = Poll.objects.filter(meeting_id=meeting_id)
#     polls_json = serializers.serialize('json', polls)
#     return HttpResponse(polls_json, content_type='application/json')


class SelectsView(View):

    def get(self, request, poll_id):
        selects = Select.objects.filter(poll_id=poll_id)
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
#         meeting.save()
#         return redirect(SITE_URL + 'api/available_room/' + str(meeting.id))
#     return JsonResponse({"status": 100})


class RoomsView(APIView):
    def get(self, request, select_id):
        select = Meeting.objects.filter(id=select_id)
        if select:
            select = select[0]
            req = requests.get('http://213.233.176.40/available_rooms' +
                               '?start=' + str(select.date) + 'T' + str(select.startTime) +
                               '&end=' + str(select.date) + 'T' + str(select.endTime))
            return JsonResponse(req.json())
        # status = 100 means that this meeting doesn't exist.
        return JsonResponse({"status": 100,
                             "text": "Meeting doesn\'t exist."
                             })

    def post(self, request, select_id):
        try:
            select_id = int(request.POST['select_id'])
            room_number = int(request.POST['room_number'])
            select = None
            try:
                select = Select.objects.get(id=select_id)
            except:
                JsonResponse({
                    "status": 100,
                    "text": 'There is no this select id.'
                })
            meeting = select.poll.meeting
            if meeting:
                if meeting.room:
                    # status = 91 means that this meeting has a room.
                    return JsonResponse({
                        "status": 91,
                        "text": 'This meeting has a room.'
                    })
                req = requests.get('http://213.233.176.40/available_rooms' +
                                   '?start=' + str(meeting.date) + 'T' + str(meeting.startTime) +
                                   '&end=' + str(meeting.date) + 'T' + str(meeting.endTime))
                availableRooms = req.json()['availableRooms']
                if room_number not in availableRooms:
                    # status = 90 means that this room has been reserved when you want to reserve it.
                    return JsonResponse({"status": 90,
                                         "text": 'This room reserved when you want to reserve it.'})
                meeting.room = room_number
                meeting.status = 2
                meeting.save()
                res = requests.post(url='http://213.233.176.40/rooms/210/reserve',
                              data={
                                  "username": 'mh.omidi',
                                  "start": str(meeting.date) + 'T' + str(meeting.startTime),
                                  "end": str(meeting.date) + 'T' + str(meeting.endTime),
                              }
                        )
                # print(str(meeting.date) + 'T' + str(meeting.startTime))
                # print(str(meeting.date) + 'T' + str(meeting.endTime))
                # print(str(res.json()))
                return JsonResponse({
                    "status": 200,
                    "text": 'Room reserved successfully'

                })
            # status = 100 means that this meeting doesn't exist.
            return JsonResponse({"status": 100,
                                 "text": "Meeting doesn\'t exist."
                                 })
        except:
            return JsonResponse({"status": 0,
                                 "text": 'An Exception occure, please try again.'})

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
#         meeting.save()
#         return redirect(SITE_URL + 'api/show_meeting/' + str(meeting_id))
#     # status = 100 means that this meeting doesn't exist.
#     return JsonResponse({"status": 100})

class PollView(APIView):
    def get(self, request, poll_id):
        poll = Poll.objects.filter(id=poll_id)
        if poll:
            poll_json = serializers.serialize('json', poll)
            return HttpResponse(poll_json, content_type='application/json')
        return JsonResponse({"status": 20,
                             "text": 'Poll doesn\'t exist.'
                             })




def showMeeting(request, meeting_id):
    meeting = Meeting.objects.filter(id=meeting_id)
    if meeting:
        meeting_json = serializers.serialize('json', meeting)
        XS_SHARING_ALLOWED_ORIGINS = '*'
        XS_SHARING_ALLOWED_METHODS = ['POST', 'GET', 'OPTIONS', 'PUT', 'DELETE']
        response = HttpResponse(meeting_json, content_type='application/json')
        # response['Access-Control-Allow-Origin'] = XS_SHARING_ALLOWED_ORIGINS
        # response['Access-Control-Allow-Methods'] = ",".join(XS_SHARING_ALLOWED_METHODS)
        return response
    # status = 100 means that this meeting doesn't exist.
    return JsonResponse({"status": 100,
                             "text": 'Meeting doesn\'t exist.'})