from django.urls import path

from . import views

urlpatterns = [
    path('', views.test),
    path('test_email/', views.test_send_email),
]
