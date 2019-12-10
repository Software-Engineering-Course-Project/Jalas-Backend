from django.urls import path

from . import views

urlpatterns = [
    path('show_log/', views.ShowLogs.as_view()),
]
