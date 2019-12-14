import datetime
import json

from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from jalas_back.HttpResponces import HttpResponse404Error
from meeting.models import Meeting
from poll.Serializer import SelectSerializer
from poll.models import Poll, Select, MeetingParticipant, SelectUser


class PollsView(APIView):
    def get(self, request, meeting_id):
        try:
            polls = Poll.objects.filter(meeting_id=meeting_id)
            polls_json = serializers.serialize('json', polls)
            return HttpResponse(polls_json, content_type='application/json')
        except:
            return HttpResponse404Error(
                "This poll doesn\'t exist."
            )


class SelectsView(APIView):

    def get(self, request, poll_id):
        try:
            selects = Select.objects.filter(poll_id=poll_id)
            selects_json = SelectSerializer.makeSerial(selects)
            return HttpResponse(selects_json, content_type='application/json')
        except:
            return HttpResponse404Error(
                "This poll doesn\'t exist."
            )


class PollView(APIView):
    def get(self, request, poll_id):
        try:
            poll = Poll.objects.get(id=poll_id)
            poll_json = serializers.serialize('json', [poll])
            return HttpResponse(poll_json, content_type='application/json')
        except:
            return HttpResponse404Error({
                'this poll doesn\'t exist.'
            })


class CreatePoll(APIView):
    def post(self, request):
        title = request.GET['title']
        text = request.GET['text']
        user = User.objects.get(username='admin')
        participants = request.GET['participants']
        participants = json.loads(participants)
        participants = participants['participants']
        selects = request.GET['selects']
        selects = json.loads(selects)
        meeting = Meeting(title=title, text=text, owner=user)
        meeting.save()
        poll = Poll(title=title, text=text, meeting=meeting)
        poll.save()
        for participant in participants:
            try:
                user = User.objects.get(email=participant)
                meetingParticipant = MeetingParticipant(meeting=meeting, participant=user)
                meetingParticipant.save()
            except:
                user = User(username=participant, email=participant, password='')
                user.save()
                meetingParticipant = MeetingParticipant(meeting=meeting, participant=user)
                meetingParticipant.save()

        for select in selects:
            date = datetime.datetime.strptime(select['date'], '%d-%m-%Y')
            startTime = datetime.datetime.strptime(select['start_time'], '%H:%M')
            endTime = datetime.datetime.strptime(select['end_time'], '%H:%M')
            select = Select(date=date, startTime=startTime, endTime=endTime, poll=poll)
            select.save()
        poll_json = serializers.serialize('json', [poll])
        return HttpResponse(poll_json, content_type='application/json')


class VotingView(APIView):
    def get(self, request, poll_id):
        try:
            selects = Select.objects.filter(poll_id=poll_id)
            selects_json = SelectSerializer.makeSerial(selects)
            return HttpResponse(selects_json, content_type='application/json')
        except:
            return HttpResponse404Error(
                "This poll doesn\'t exist."
            )

    def post(self, request, poll_id):
        try:
            selects = request.GET['selects']
            selects = json.loads(selects)
            name = request.GET['name']
            user = User.objects.get(username='admin')
            # TODO: create selcetUSer
            for key in selects.keys():
                try:
                    select = Select.objects.get(id=int(key))
                    try:
                        selectUser = SelectUser.objects.get(select=select, user=user, name=name)
                        selectUser.agreement = selects[key]
                        selectUser.save()
                    except:
                        selectUser = SelectUser(select=select, user=user, agreement=selects[key], name=name)
                        selectUser.save()
                except Exception as e:
                    print(e.__traceback__)
                    return  HttpResponse404Error(
                        "One of the options not found."
                    )
            return HttpResponse(
                "Submit successfully"
            )
        except:
            return HttpResponse404Error(
                "This poll doesn\'t exist."
            )