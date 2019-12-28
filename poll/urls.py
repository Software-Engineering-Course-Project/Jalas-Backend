from django.urls import path

from . import views

urlpatterns = [
    path('polls/', views.PollsView.as_view()),
    path('selects/<int:poll_id>', views.SelectsView.as_view()),
    path('poll/<int:poll_id>', views.PollView.as_view()),
    path('create_poll/', views.CreatePoll.as_view()),
    path('vote/<int:poll_id>', views.VotingView.as_view()),
    path('get_voter/<int:poll_id>', views.GetVoterName.as_view()),
    path('get_last_poll/', views.GetLastPoll.as_view()),
    path('add_comment/<int:poll_id>', views.AddCommentView.as_view()),
    path('modify/<int:poll_id>', views.ModifiedPollView.as_view()),
    path('get_comment/<int:poll_id>', views.GetCommentView.as_view()),
    path('can_vote/<int:poll_id>', views.CanVoteView.as_view()),
    path('get_participants/<int:poll_id>', views.GetParticipantsView.as_view()),
]
