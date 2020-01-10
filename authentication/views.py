import requests
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from Jalas.settings import SITE_URL
from authentication.models import User
from jalas_back.HttpResponces import HttpResponse404Error


class LoginView(APIView):

    def get(self, request, username, password):
        res = requests.post(SITE_URL + 'api/auth/get_token/',
                            json={
                                "username": username,
                                "password": password
                            }
                            )
        if res.status_code != 200:
            return HttpResponse404Error(
                "User not found"
            )
        return HttpResponse(res, content_type='application/json')


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        email = request.data.get('email', '')
        try:
            if username != '' and password != '' and email != '':
                User.objects.create(username=username, password=password, email=email)
                return HttpResponse(
                    "ثبت نام شما با موفقیت انجام شد"
                )
            return HttpResponse(
                "ثبت نام شما با مشکل مواجه شد"
            )
        except:
            return HttpResponse(
                "ثبت نام شما ناموفق بود."
            )

