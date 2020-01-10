from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns = [
    path('get_token/', jwt_views.TokenObtainPairView.as_view(), name='api_token_auth'),
    path('login/<slug:username>/<slug:password>/', views.LoginView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('get_user/', ),
]