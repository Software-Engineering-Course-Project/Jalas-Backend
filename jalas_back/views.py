import json

import requests
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from Jalas.settings import SITE_URL
from jalas_back.Serializer import SelectSerializer
from jalas_back.models import Meeting, Poll, Select


def test(request):
    req = requests.get('http://213.233.176.40/available_rooms' +
    '?start=2019-09-13T19:00:00&end=2019-09-13T20:00:00')

    print(type(req.json()))
    return HttpResponse(str(req.json()))


def getMeeting(request):
    meetings = Meeting.objects.all()
    meetings_json = serializers.serialize('json', meetings)
    return HttpResponse(meetings_json, content_type='application/json')


def getPolls(request, meeting_id):
    polls = Poll.objects.filter(meeting_id=meeting_id)
    polls_json = serializers.serialize('json', polls)
    return HttpResponse(polls_json, content_type='application/json')


def getSelect(request, poll_id):
    selects = Select.objects.filter(poll_id=poll_id)
    selects_json = SelectSerializer.makeSerial(selects)
    return HttpResponse(selects_json, content_type='application/json')


def setMeetingTime(request, select_id):
    select = Select.objects.filter(id=select_id)
    if select:
        select = select[0]
        meeting = select.poll.meeting
        meeting.date = select.date
        meeting.startTime = meeting.startTime
        meeting.endTime = meeting.endTime
        meeting.save()
        return redirect(SITE_URL + 'api/get_available_room/' + str(meeting.id))
    return HttpResponse('{"err" : 100}')

def getAvailaibleRoom(request, meeting_id):
    meeting = Meeting.objects.filter(id=meeting_id)
    if meeting:
        meeting = meeting[0]
        if not meeting.date or meeting.endTime or meeting.startTime:
            # err = 100 means that this meeting doesn't exist.
            return HttpResponse('{"err" : 100}')
        req = requests.get('http://213.233.176.40/available_rooms' +
                           '?start=' + str(meeting.date) + 'T' + str(meeting.startTime) +
                           '&end=' + str(meeting.date) + 'T' + str(meeting.endTime))
        return HttpResponse(str(req.json()))
    # err = 100 means that this meeting doesn't exist.
    return HttpResponse('{"err" : 100}')


def setMeetingRoom(request, meeting_id, room_number):
    meeting = Meeting.objects.filter(id=meeting_id)
    if meeting:
        meeting = meeting[0]
        if meeting.room:
            # err = 91 means that this meeting has a room.
            return HttpResponse('{"err" : 91}')
        req = requests.get('http://213.233.176.40/available_rooms' +
                           '?start=' + str(meeting.date) + 'T' + str(meeting.startTime) +
                           '&end=' + str(meeting.date) + 'T' + str(meeting.endTime))
        availableRooms = req.json()['availableRooms']
        if room_number not in availableRooms:
            # err = 90 means that this room has been reserved when you want to reserve it.
            return HttpResponse('{"err" : 90}')
        meeting.room = room_number
        meeting.status = 2
        meeting.save()
        return redirect(SITE_URL + 'api/show_meeting/' + str(meeting_id))
    # err = 100 means that this meeting doesn't exist.
    return HttpResponse('{"err" : 100}')


def showMeeting(request, meeting_id):
    meeting = Meeting.objects.filter(id=meeting_id)
    if meeting:
        meeting_json = serializers.serialize('json', meeting)
        return HttpResponse(meeting_json, content_type='application/json')
    # err = 100 means that this meeting doesn't exist.
    return HttpResponse('{"err" : 100}')