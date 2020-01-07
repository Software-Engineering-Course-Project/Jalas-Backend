from django.urls import path

from . import views

urlpatterns = [
    path('get_comments/<int:poll_id>', views.GetCommentView.as_view()),
    path('add_comment/<int:poll_id>', views.AddCommentView.as_view()),
]