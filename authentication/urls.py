from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('get_token/', obtain_auth_token, name='api_token_auth'),
    path('login/<slug:username>/<slug:password>/', views.LoginView.as_view())
]