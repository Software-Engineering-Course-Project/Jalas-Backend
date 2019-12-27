import datetime
import json

from django.contrib.auth.models import User
from django.core import serializers
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView, Response

from Jalas import settings
from jalas_back.HttpResponces import HttpResponse404Error
from meeting.models import Meeting
from poll.Serializer import SelectSerializer, CommentSerializer
from poll.models import Poll, Select, MeetingParticipant, SelectUser, Comment
from rest_framework.permissions import IsAuthenticated


class PollsView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            polls = Poll.objects.filter(meeting__owner=request.user)
            polls_json = serializers.serialize('json', polls)
            return HttpResponse(polls_json, content_type='application/json')
        except:
            return HttpResponse404Error(
                "This poll doesn\'t exist."
            )


class SelectsView(APIView):
    permission_classes = (IsAuthenticated,)

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

    permission_classes = (IsAuthenticated,)

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

    permission_classes = (IsAuthenticated,)
    def post(self, request):
        title = request.data.get('title')
        text = request.data.get('text')
        link = request.data.get('link', 'No link')
        user = request.user
        participants = request.data.get('participants', [])
        selects = request.data.get('selects')
        meeting = Meeting(title=title, text=text, owner=user)
        meeting.save()
        poll = Poll(title=title, text=text, meeting=meeting)
        poll.save()
        meetingParticipant = MeetingParticipant(meeting=meeting, participant=user)
        meetingParticipant.save()
        link += str(poll.id)
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
        send_mail(
            subject=title,
            message=link,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=participants
        )
        try:
            return HttpResponse(poll_json, content_type='application/json')

        except Exception as e:
            print(e)
            return HttpResponse404Error(
                "This poll doesn\'t exist."
            )


class VotingView(APIView):


    permission_classes = (IsAuthenticated,)

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
            selects = request.data.get('vote')
            name = request.data.get('name')
            user = request.user
            poll = Poll.objects.get(id=poll_id)
            poll_selects = poll.selects.all()
            # TODO: create selcetUSer
            for index, val in enumerate(selects):
                if val == 1:
                    try:
                        try:
                            selectUser = SelectUser.objects.get(select=poll_selects[index], user=user, name=name)
                            selectUser.agreement = 2
                            selectUser.save()
                        except:
                            selectUser = SelectUser(select=poll_selects[index], user=user, agreement=2, name=name)
                            selectUser.save()
                    except Exception as e:
                        return  HttpResponse404Error(
                            "One of the options not found."
                        )
                if val == 0:
                    try:
                        try:
                            selectUser = SelectUser.objects.get(select=poll_selects[index], user=user, name=name)
                            selectUser.agreement = 1
                            selectUser.save()
                        except:
                            selectUser = SelectUser(select=poll_selects[index], user=user, agreement=1, name=name)
                            selectUser.save()
                    except Exception as e:
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


class GetVoterName(APIView):


    permission_classes = (IsAuthenticated,)

    def get(self, request, poll_id):
        try:
            names = {}
            poll = Poll.objects.get(id=poll_id)
            poll_selects = poll.selects.all()
            for index, select in enumerate(poll_selects):
                selectUsers = SelectUser.objects.filter(select=select)
                for s in selectUsers:
                    if s.name in names.keys():
                        if s.agreement == 2:
                            names[s.name][index] = 1
                    else:
                        names[s.name] = [0 for i in range(len(poll_selects))]
                        if s.agreement == 2:
                            names[s.name][index] = 1
            res = []
            for name in names.keys():
                ss = {}
                ss['name'] = name
                ss['votes'] = names[name]
                res.append(ss)
            return HttpResponse(json.dumps(res), content_type='application/json')

        except:
            return HttpResponse404Error(
                "This poll doesn\'t exist."
            )


class GetLastPoll(APIView):
    def get(self, request):
        try:
            poll = Poll.objects.last()
            poll = serializers.serialize('json', [poll])
            return HttpResponse(poll, content_type='application/json')
        except:
            return HttpResponse404Error(
                "No poll doesn\'t exist."
            )

class AddCommentView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request, poll_id):
        try:
            poll = Poll.objects.get(id=poll_id)
            meeting = poll.meeting
            text = request.data.get('text')
            owner = request.user
            if not MeetingParticipant.objects.filter(participant=owner, meeting=meeting):
                return HttpResponse404Error(
                    "You don\'t have permission to comment on this poll"
                )

            comment = Comment(owner=owner, poll=poll, text=text)
            comment.save()
            comment_json = serializers.serialize('json', [comment])
            return HttpResponse(comment_json, content_type='application/json')
        except:
            return HttpResponse404Error(
                "No poll doesn\'t exist."
            )


class GetCommentView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, poll_id):
        comments = Comment.objects.filter(poll_id=poll_id)
        comments_json = CommentSerializer.makeSerial(comments)
        return HttpResponse(comments_json, content_type='application/json')


class ModifiedPollView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, poll_id):
        try:
           poll = Poll.objects.get(id=poll_id, meeting__owner=request.user)
        except:
            return HttpResponse404Error(
                "No poll doesn\'t exist or you can\'t access to modified this poll."
            )
        title = request.data.get('title', None)
        text = request.data.get('text', None)
        poll.text = text
        poll.title = title
        poll.save()
        meeting = poll.meeting
        meeting.text = text
        meeting.title = title
        meeting.save()
        link = request.data.get('link', 'No link')
        new_participants = request.data.get('participants', [])
        selects = request.data.get('selects')
        meetingParticipants = MeetingParticipant.objects.filter(meeting=poll.meeting)
        old_participants = []
        for par in meetingParticipants:
            old_participants.append(par.participant.email)
        old_participants = set(old_participants)
        new_participants = set(new_participants)
        old_new = old_participants.difference(new_participants)
        new_old = new_participants.difference(old_participants)
        for par_email in old_new:
            try:
                par = User.objects.get(email=par_email)
                meet_par = MeetingParticipant.objects.get(participant=user, meeting=poll.meeting)
                meet_par.delete()
            except:
                pass
        for par_email in new_old:
            try:
                user = User.objects.get(email=par_email)
                meetingParticipant = MeetingParticipant(meeting=poll.meeting, participant=user)
                meetingParticipant.save()
            except:
                user = User(username=par_email, email=par_email, password='')
                user.save()
                meetingParticipant = MeetingParticipant(meeting=poll.meeting, participant=user)
                meetingParticipant.save()
        old_selects = poll.selects.all()
        new_selects = []
        for select in selects:
            date = datetime.datetime.strptime(select['date'], '%d-%m-%Y')
            startTime = datetime.datetime.strptime(select['start_time'], '%H:%M')
            endTime = datetime.datetime.strptime(select['end_time'], '%H:%M')
            try:
                old_select = Select.objects.get(date=date, startTime=startTime, endTime=endTime, poll=poll)
                new_selects.append(old_select)
            except:
                new_select = Select(date=date, startTime=startTime, endTime=endTime, poll=poll)
                new_select.save()
                new_selects.append(new_select)
        for old_select in old_selects:
            flag = True
            for new_select in new_selects:
                if old_select.id == new_select.id:
                    flag = False
            if flag:
                old_select.delete()

        poll_json = serializers.serialize('json', [poll])
        participants = old_participants.union(new_participants)
        send_mail(
            subject=title,
            message='This poll was changed \n' + link,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=participants
        )
        return HttpResponse(poll_json, content_type='application/json')
