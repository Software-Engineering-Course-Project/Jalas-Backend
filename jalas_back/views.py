import requests
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
import json

# Create your views here.
from jalas_back.models import Meeting


def hello(request):
    req = requests.get('http://213.233.176.40/available_rooms' +
    '?start=2019-09-13T19:00:00&end=2019-09-13T20:00:00')

    print(type(req.json()))
    return HttpResponse(str(req.json()))

def getMeeting(request):
    meetings = Meeting.objects.all()
    meetings_json = serializers.serialize('json', meetings)
    return HttpResponse(meetings_json, content_type='application/json')