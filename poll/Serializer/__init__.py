import json

from django.core import serializers


class SelectSerializer:

    @staticmethod
    def makeSerial(selects):
        selects_json = serializers.serialize('json', selects)
        selects_list = json.loads(selects_json)
        for index, val in enumerate(selects_list):
            selects_list[index]['fields']['agree'] = selects[index].agree if selects[index].agree else 0
            selects_list[index]['fields']['disagree'] = selects[index].disagree if selects[index].disagree else 0
        return json.dumps(selects_list)

class CommentSerializer:

    @staticmethod
    def makeSerial(comments):
        comments_json = serializers.serialize('json', comments)
        comments_list = json.loads(comments_json)
        for index, val in enumerate(comments_list):
            comments_list[index]['fields']['username'] = comments[index].owner.username if comments[index].owner.username else 'Unknown'
        return json.dumps(comments_list)


class ShowPollSerializer:

    @staticmethod
    def makeSerial(poll):
        poll_json = serializers.serialize('json', [poll])
        poll_list = json.loads(poll_json)
        for index, val in enumerate(poll_list):
            poll_list[index]['fields']['state'] = True if poll.meeting.status != 1 else False
        return json.dumps(poll_list)