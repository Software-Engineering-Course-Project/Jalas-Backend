from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from comment.models import Comment
from jalas_back.HttpResponces import HttpResponse404Error
from poll.Serializer import CommentSerializer
from poll.models import Poll, MeetingParticipant


class AddCommentView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request, poll_id):
        try:
            poll = Poll.objects.get(id=poll_id)
            meeting = poll.meeting
            text = request.data.get('text')
            owner = request.user
            if not MeetingParticipant.objects.filter(participant=owner, meeting=meeting):
                return HttpResponse404Error(
                    "You don\'t have permission to comment on this poll"
                )

            comment = Comment(owner=owner, poll=poll, text=text)
            comment.save()
            comment_json = serializers.serialize('json', [comment])
            return HttpResponse(comment_json, content_type='application/json')
        except:
            return HttpResponse404Error(
                "No poll doesn\'t exist."
            )


class GetCommentView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, poll_id):
        comments = Comment.objects.filter(poll_id=poll_id)
        comments_replies = []
        for comment in comments:
            comments_replies.append(comment)
            reps = comment.get_replies
            comments_replies += reps
        comments_json = CommentSerializer.makeSerial(comments_replies)
        return HttpResponse(comments_json, content_type='application/json')


class AddReplyView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return HttpResponse404Error(
                "You don\'t have permission to comment on this poll"
            )
        poll = comment.get_poll
        meeting = poll.meeting
        text = request.data.get('text')
        owner = request.user
        if not MeetingParticipant.objects.filter(participant=owner, meeting=meeting):
            return HttpResponse404Error(
                "You don\'t have permission to comment on this poll"
            )

        reply = Comment(owner=owner, poll=None, text=text, parent=comment, level=comment.level + 1)
        reply.save()
        reply_json = serializers.serialize('json', [reply])
        return HttpResponse(reply_json, content_type='application/json')


class DeleteCommentView(APIView):

    def get(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return HttpResponse404Error(
                "This comment not found."
            )
        comment.delete()
        return HttpResponse(
            'Comment deleted successfully'
        )


class EditCommentView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return HttpResponse404Error(
                "No comment doesn\'t exist."
            )
        if request.user != comment.owner:
            return HttpResponse404Error(
                "You don\'t have permission to comment on this poll"
            )
        text = request.data.get('text')
        comment.text = text
        comment.save()
        comments_json = CommentSerializer.makeSerial([comment])
        return HttpResponse(
            comments_json, content_type='application/json'
        )
