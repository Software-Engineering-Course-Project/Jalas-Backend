from django.core import serializers
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from configurations.models import Configuration


class GetConfigView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):
        try:
            conf = Configuration.objects.get(user=request.user)
        except:
            conf = Configuration(user=request.user)
            conf.save()
        conf_json = serializers.serialize('json', [conf])
        return HttpResponse(conf_json, content_type='json/application')

class SetConfigView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request):
        try:
            conf = Configuration.objects.get(user=request.user)
        except:
            conf = Configuration(user=request.user)
            conf.save()
        arrange_meeting = request.data.get('arrange_meeting', False)
        add_option = request.data.get('add_option', False)
        new_vote = request.data.get('new_vote', False)
        remove_option = request.data.get('remove_option', False)
        add_new_participant = request.data.get('add_new_participant', False)
        close_poll = request.data.get('close_poll', False)
        close_meeting = request.data.get('close_meeting', False)
        conf.arrange_meeting = arrange_meeting
        conf.add_option = add_option
        conf.new_vote = new_vote
        conf.remove_option = remove_option
        conf.add_new_participant = add_new_participant
        conf.close_poll = close_poll
        conf.close_meeting = close_meeting
        conf.save()
        conf_json = serializers.serialize('json', [conf])
        return HttpResponse(conf_json, content_type='json/application')

