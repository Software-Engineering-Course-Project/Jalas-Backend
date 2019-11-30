from django.urls import path

from . import views

urlpatterns = [
    path('', views.test),
    path('meeting/', views.getMeeting),
    path('get_polls/<int:meeting_id>', views.getPolls),
    path('get_selects/<int:poll_id>', views.getSelect),
]
