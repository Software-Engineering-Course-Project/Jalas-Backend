import requests
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from Jalas.settings import SITE_URL
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
        username = request.data.get('username', None)
        password = request.data.get('password', None)
