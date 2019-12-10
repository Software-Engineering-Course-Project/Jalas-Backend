from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from jalas_back.HttpResponces import HttpResponse404Error
from meeting.models import Meeting
from poll.models import Select


class MeetingsView(APIView):
    def get(self, request):
        meetings = Meeting.objects.all()
        meetings_json = serializers.serialize('json', meetings)
        return HttpResponse(meetings_json, content_type='application/json')


class ShowMeeting(APIView):
    def get(self, request, select_id):
        try:
            select = Select.objects.get(id=select_id)
            meeting = select.poll.meeting
            meeting_json = serializers.serialize('json', [meeting])
            return HttpResponse(meeting_json, content_type='application/json')
        except:
            return HttpResponse404Error(
                "This select_id doesn\'t exist."
            )
