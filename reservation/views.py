import requests
from django.core import serializers
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from Jalas import settings
from data_access.accress_logic import SetReservationTimes
from jalas_back.HttpResponces import HttpResponse500Error, HttpResponse404Error, HttpResponse405Error
from poll.models import Select


class RoomsView(APIView):
    def get(self, request, select_id):
        try:
            select = Select.objects.get(id=select_id)
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
            select = Select.objects.get(id=select_id)
            meeting = select.poll.meeting
            meeting.startTime = select.startTime
            meeting.endTime = select.endTime
            meeting.date = select.date
            meeting.save()
            SetReservationTimes.startTime(meeting.id)
            return HttpResponse("Set date and time successfully")
        except:
            return HttpResponse404Error({
                "select or poll not found"
            })


class SetRoomView(APIView):
    def get(self, request, room, select_id):
        try:
            select = Select.objects.get(id=select_id)
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
                    select = Select.objects.get(id=select_id)
                    meeting = select.poll.meeting
                    if meeting.isCancel:
                        meeting_json = serializers.serialize('json', [meeting])
                        return HttpResponse(meeting_json, content_type='application/json')

                    if res.status_code == 200:
                        meeting.room = room
                        meeting.status = 2
                        SetReservationTimes.endTime(meeting.id)
                        meeting.save()
                        self.sendMail([meeting.owner.email, ], meeting)
                        meeting_json = serializers.serialize('json', [meeting])
                        return HttpResponse(meeting_json, content_type='application/json')
                    elif res.status_code == 400:
                        return HttpResponse404Error({
                            "Room Not found"
                        })
                except:
                    select = Select.objects.get(id=select_id)
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



class SetCancel(APIView):
    def get(self, request, select_id):
        try:
            select = Select.objects.get(id=select_id)
            meeting = select.poll.meeting
            meeting.isCancel = True
            meeting.status = 4
            meeting.room = None
            meeting.save()
            SetReservationTimes.delete(meeting)
            meeting_json = serializers.serialize('json', [meeting])
            return HttpResponse(meeting_json, content_type='application/json')

        except:
            return HttpResponse404Error({
                'this select doesn\'t exist.'
            })
