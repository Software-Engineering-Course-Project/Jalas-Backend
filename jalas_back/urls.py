from django.urls import path

from . import views

urlpatterns = [
    path('', views.test),
    path('meeting/', views.MeetingView.as_view()),
    path('polls/<int:meeting_id>', views.PollView.as_view()),
    path('selects/<int:poll_id>', views.SelectView.as_view()),
    path('available_room/<int:meeting_id>/', views.RoomView.as_view()),
    path('show_meeting/<int:meeting_id>', views.showMeeting),
]
