import requests
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse

# Create your views here.

from rest_framework.views import APIView
from Jalas import settings


def test(request):
    ret = ''
    try:
        req = requests.get('http://213.233.176.40/available_rooms' +
        '?start=2019-11-30T12:30:00&end=2019-11-30T14:30:00')
        ret = req.json()
    except:
        return JsonResponse({"status": 10})
    return JsonResponse(ret)


def test_send_email(request):
    send_mail('salam', 'jalas', settings.DEFAULT_FROM_EMAIL, ['mohammadhadi.omidi92@gmail.com',], fail_silently=False)
    return HttpResponse("ssss")

