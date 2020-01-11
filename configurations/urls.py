from django.urls import path

from . import views

urlpatterns = [
    path('get/', views.GetConfigView.as_view()),
    path('set/', views.SetConfigView.as_view()),
]
