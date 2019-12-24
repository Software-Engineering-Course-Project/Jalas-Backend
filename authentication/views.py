import requests
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from Jalas.settings import SITE_URL


class LoginView(APIView):

    def get(self, request, username, password):
        res = requests.post(SITE_URL + 'api/auth/get_token/',
                            json={
                                "username": username,
                                "password": password
                            }
                            )
        return HttpResponse(res, content_type='application/json')