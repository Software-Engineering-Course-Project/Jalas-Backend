import datetime
import json

from django.core import serializers
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from Jalas import settings
from authentication.models import User
from jalas_back.HttpResponces import HttpResponse404Error, HttpResponse999Error
from meeting.models import Meeting
from poll.Serializer import SelectSerializer, CommentSerializer, ShowPollSerializer, ShowPollsSerializer
from poll.emails import send_email_arrange_meeting, send_email_add_option, send_email_add_participant, \
    send_email_new_vote, send_email_close_poll
from poll.functions import check_poll_close
from poll.models import Poll, Select, MeetingParticipant, SelectUser
from rest_framework.permissions import IsAuthenticated


class PollsView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            # polls = Poll.objects.filter(meeting__owner=request.user)
            meetingParticipants = MeetingParticipant.objects.filter(participant=request.user)
            polls = []
            for mp in meetingParticipants:
                polls.append(mp.meeting.polls.all()[0])
            polls_json = ShowPollsSerializer.makeSerial(polls, request.user)
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
            if poll.meeting.owner.username != request.user.username:
                return HttpResponse999Error({
                    'You don\'t have access to this point.'
                })

            poll_json = ShowPollSerializer.makeSerial(poll)
            return HttpResponse(poll_json, content_type='application/json')
        except:
            return HttpResponse404Error({
                'this poll doesn\'t exist.'
            })

class GetPollTitleView(APIView):

    def get(self, request, poll_id):
        try:
            poll = Poll.objects.get(id=poll_id)
        except:
            return HttpResponse404Error({
                'this poll doesn\'t exist.'
            })

        if check_poll_close(poll):
            return HttpResponse999Error(
                "این نظرسنجی بسته شده است."
            )
        return HttpResponse(
            '{"title": "' + poll.title + '" }', content_type='application/json'
        )

class GetParticipantsView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, poll_id):
        try:
            poll = Poll.objects.get(id=poll_id)
            meeting = poll.meeting
            meetingParticipants = MeetingParticipant.objects.filter(meeting=meeting)
            participants = []
            for mp in meetingParticipants:
                if mp.participant.email != request.user.email:
                    participants.append(mp.participant.email)
            participants = {
                'participants': participants
            }
            participants_json = json.dumps(participants)
            return HttpResponse(participants_json, content_type='application/json')
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
        close_date = request.data.get('closeDate', '')
        participants = request.data.get('participants', [])
        selects = request.data.get('selects')
        meeting = Meeting(title=title, text=text, owner=user)
        meeting.save()
        poll = Poll(title=title, text=text, meeting=meeting)
        if close_date:
            poll.date_close = datetime.datetime.strptime(close_date, '%Y-%m-%d')
        poll.save()
        meetingParticipant = MeetingParticipant(meeting=meeting, participant=user)
        meetingParticipant.save()
        link += str(poll.id)
        self.create_participants(meeting, participants, user)
        self.createOptions(poll, selects)

        check_poll_close(poll)
        poll_json = serializers.serialize('json', [poll])
        send_email_arrange_meeting(user, title, link, participants)

        try:
            return HttpResponse(poll_json, content_type='application/json')

        except Exception as e:
            print(e)
            return HttpResponse404Error(
                "This poll doesn\'t exist."
            )

    def createOptions(self, poll, selects):
        for select in selects:
            date = datetime.datetime.strptime(select['date'], '%Y-%m-%d')
            startTime = datetime.datetime.strptime(select['start_time'], '%H:%M')
            endTime = datetime.datetime.strptime(select['end_time'], '%H:%M')
            select = Select(date=date, startTime=startTime, endTime=endTime, poll=poll)
            select.save()

    def create_participants(self, meeting, participants, user):
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


class VotingView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, poll_id):
        try:
            poll = Poll.objects.get(id=poll_id)

            if check_poll_close(poll):
                return HttpResponse999Error(
                    "این نظرسنجی بسته شده است."
                )
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

        except:
            return HttpResponse404Error(
                "This poll doesn\'t exist."
            )

        if check_poll_close(poll):
            return HttpResponse999Error(
                "این نظرسنجی بسته شده است."
            )
        poll_selects = poll.selects.all()
        for index, val in enumerate(selects):
            try:
                try:
                    selectUser = SelectUser.objects.get(select=poll_selects[index], user=user, name=name)
                    selectUser.agreement = val + 1
                    selectUser.save()
                except:
                    selectUser = SelectUser(select=poll_selects[index], user=user, agreement=val + 1, name=name)
                    selectUser.save()
            except Exception as e:
                return  HttpResponse404Error(
                    "One of the options not found."
                )
        send_email_new_vote(user, poll, user.email)
        return HttpResponse(
            "Submit successfully"
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
                        if s.agreement == 1:
                            names[s.name][index] = 0
                        elif s.agreement == 2:
                            names[s.name][index] = 1
                        elif s.agreement == 3:
                            names[s.name][index] = 2
                        else:
                            names[s.name][index] = -1

                    else:
                        names[s.name] = [-1 for i in range(len(poll_selects))]
                        if s.agreement == 1:
                            names[s.name][index] = 0
                        elif s.agreement == 2:
                            names[s.name][index] = 1
                        elif s.agreement == 3:
                            names[s.name][index] = 2
                        else:
                            names[s.name][index] = -1
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
        close_date = request.data.get('closeDate', '')
        poll.text = text
        poll.title = title
        if close_date:
            poll.date_close = datetime.datetime.strptime(close_date, '%Y-%m-%d')
        poll.status = False
        poll.save()
        meeting = poll.meeting
        meeting.text = text
        meeting.title = title
        meeting.save()
        link = request.data.get('link', 'No link')
        new_participants = request.data.get('participants', [])
        new_participants.append(request.user.email)
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
                meet_par = MeetingParticipant.objects.get(participant=par, meeting=poll.meeting)
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
        has_new_select = False
        for select in selects:
            date = datetime.datetime.strptime(select['date'], '%Y-%m-%d')
            startTime = datetime.datetime.strptime(select['start_time'], '%H:%M')
            endTime = datetime.datetime.strptime(select['end_time'], '%H:%M')
            try:
                old_select = Select.objects.get(date=date, startTime=startTime, endTime=endTime, poll=poll)
                new_selects.append(old_select)
                has_new_select = True
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
                old_select.delete_me(request.user, title, link)
        poll_json = serializers.serialize('json', [poll])
        participants = old_participants.union(new_participants)
        if has_new_select:
            send_email_add_option(request.user, title, link, participants)
        if new_old:
            send_email_add_participant(request.user, title, link, participants)
        return HttpResponse(poll_json, content_type='application/json')

class CanVoteView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, poll_id):
        try:
            poll = Poll.objects.get(id=poll_id)
            meetingParticipant = MeetingParticipant.objects.get(participant=request.user, meeting=poll.meeting)
        except:
            return HttpResponse(
                    "{\"value\": 2}", content_type='application/json'
                )

        selectUser = SelectUser.objects.filter(user=request.user, select__poll_id=poll_id)
        if selectUser:
            return HttpResponse(
                "{\"value\": 0}", content_type='application/json'
            )
        return HttpResponse(
                "{\"value\": 1}", content_type='application/json'
            )


class ClosePollView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, poll_id):
        try:
            poll = Poll.objects.get(id=poll_id)
        except:
            return HttpResponse404Error(
                "No poll doesn\'t exist."
            )
        poll.status = True
        poll.save()
        meetPars = MeetingParticipant.objects.filter(meeting=poll.meeting)
        send_email_close_poll(request.user, poll, meetPars)
        poll_json = serializers.serialize('json', [poll])
        return HttpResponse(
            "نظرسنجی با موفقیت بسته شد."
        )


class GetUserNameInAPollView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, poll_id):
        selectUsers = SelectUser.objects.filter(select__poll_id=poll_id)
        name = ''
        for su in selectUsers:
            if su.user == request.user:
                name = su.name
                break
        if name:
            return HttpResponse(
                '{"name": "' + name + '"}', content_type='application/json'
            )
        return HttpResponse404Error(
            "این کاربر تا به حال رای نداده است."
        )
