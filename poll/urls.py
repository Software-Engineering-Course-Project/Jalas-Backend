from django.urls import path

from . import views

urlpatterns = [
    path('polls/<int:meeting_id>', views.PollsView.as_view()),
    path('selects/<int:poll_id>', views.SelectsView.as_view()),
    path('poll/<int:poll_id>', views.PollView.as_view()),
    path('create_poll/', views.CreatePoll.as_view()),
    path('vote/<int:poll_id>', views.VotingView.as_view()),
]
