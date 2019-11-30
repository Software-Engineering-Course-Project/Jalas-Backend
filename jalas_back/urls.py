from django.urls import path

from . import views

urlpatterns = [
    path('', views.test),
    path('meeting/', views.getMeeting),
    path('get_polls/<int:meeting_id>', views.getPolls),
    path('get_selects/<int:poll_id>', views.getSelect),
    path('set_meeting_time/<int:select_id>/', views.setMeetingTime),
    path('get_available_room/<int:meeting_id>/', views.getAvailaibleRoom),
    path('set_meeting_room/<int:meeting_id>/<int:room_number>/', views.setMeetingRoom),
    path('show_meeting/<int:meeting_id>', views.showMeeting),
]
