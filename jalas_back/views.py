import requests
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from jalas_back.Serializer import SelectSerializer
from jalas_back.models import Meeting, Poll, Select, SelectUser


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
