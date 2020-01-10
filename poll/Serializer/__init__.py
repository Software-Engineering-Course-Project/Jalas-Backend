import json

from django.core import serializers

from poll.functions import check_poll_close


class SelectSerializer:

    @staticmethod
    def makeSerial(selects):
        selects_json = serializers.serialize('json', selects)
        selects_list = json.loads(selects_json)
        for index, val in enumerate(selects_list):
            selects_list[index]['fields']['agree'] = selects[index].agree if selects[index].agree else 0
            selects_list[index]['fields']['disagree'] = selects[index].disagree if selects[index].disagree else 0
            selects_list[index]['fields']['if_needed'] = selects[index].ifNeeded if selects[index].ifNeeded else 0
        return json.dumps(selects_list)

class CommentSerializer:

    @staticmethod
    def makeSerial(comments, user):
        comments_json = serializers.serialize('json', comments)
        comments_list = json.loads(comments_json)
        for index, val in enumerate(comments_list):
            comments_list[index]['fields']['username'] = comments[index].owner.username if comments[index].owner.username else 'Unknown'
            comments_list[index]['fields']['can_edit'] = comments[index].can_edit(user)
            comments_list[index]['fields']['can_delete'] = comments[index].can_delete(user)
        return json.dumps(comments_list)


class ShowPollSerializer:

    @staticmethod
    def makeSerial(poll):
        poll_json = serializers.serialize('json', [poll])
        poll_list = json.loads(poll_json)
        for index, val in enumerate(poll_list):
            poll_list[index]['fields']['state'] = True if poll.meeting.status != 1 else False
        return json.dumps(poll_list)


class ShowPollsSerializer:

    @staticmethod
    def makeSerial(polls, user):
        for poll in polls:
            check_poll_close(poll)
        poll_json = serializers.serialize('json', polls)
        poll_list = json.loads(poll_json)
        for index, val in enumerate(poll_list):
            poll_list[index]['fields']['state'] = True if polls[index].meeting.status != 1 else False
            poll_list[index]['fields']['is_owner'] = True if polls[index].meeting.owner == user else False
        return json.dumps(poll_list)
