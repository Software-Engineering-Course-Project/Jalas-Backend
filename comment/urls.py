from django.urls import path

from . import views

urlpatterns = [
    path('get/<int:poll_id>', views.GetCommentView.as_view()),
    path('add/<int:poll_id>', views.AddCommentView.as_view()),
    path('edit/<int:comment_id>', views.EditCommentView.as_view()),
    path('delete/<int:comment_id>', views.DeleteCommentView.as_view()),
    path('reply/<int:comment_id>', views.AddReplyView.as_view()),
]