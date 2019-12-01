from django.urls import path

from . import views

urlpatterns = [
    path('', views.test),
    path('meeting/', views.MeetingsView.as_view()),
    path('polls/<int:meeting_id>', views.PollsView.as_view()),
    path('selects/<int:poll_id>', views.SelectsView.as_view()),
    path('available_room/<int:meeting_id>/', views.RoomsView.as_view()),
    path('show_meeting/<int:meeting_id>', views.showMeeting),
    path('poll/<int:poll_id>', views.PollView.as_view()),
]
