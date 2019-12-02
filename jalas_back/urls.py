from django.urls import path

from . import views

urlpatterns = [
    path('', views.test),
    path('meeting/', views.MeetingsView.as_view()),
    path('polls/<int:meeting_id>', views.PollsView.as_view()),
    path('selects/<int:poll_id>', views.SelectsView.as_view()),
    path('available_room/<int:select_id>/', views.RoomsView.as_view()),
    path('show_meeting/<int:select_id>', views.showMeeting),
    path('poll/<int:poll_id>', views.PollView.as_view()),
    path('set_room/<int:room>/<int:select_id>', views.SetRoomView.as_view()),
    path('set_date/<int:select_id>/', views.SetDateView.as_view()),
    path('test_email/', views.test_send_email),
    path('set_cancel/<int:select_id>', views.SetCancel.as_view()),
]
