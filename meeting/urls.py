from django.urls import path

from . import views

urlpatterns = [
    path('meeting/', views.MeetingsView.as_view()),
    path('show_meeting/<int:select_id>', views.ShowMeeting.as_view()),
]